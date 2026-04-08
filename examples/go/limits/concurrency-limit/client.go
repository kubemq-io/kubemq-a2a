package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
	"time"
)

const (
	kubemqURL   = "http://localhost:9090"
	agentID     = "concurrency-agent-01"
	numRequests = 101
)

type result struct {
	data map[string]interface{}
	err  error
}

func sendRequest(id int, client *http.Client, wg *sync.WaitGroup, results chan<- result) {
	defer wg.Done()
	payload := map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      id,
		"method":  "message/send",
		"params": map[string]interface{}{
			"message": map[string]interface{}{
				"parts": []map[string]interface{}{{"text": fmt.Sprintf("Request #%d", id)}},
			},
		},
	}
	data, _ := json.Marshal(payload)
	resp, err := client.Post(kubemqURL+"/a2a/"+agentID, "application/json", bytes.NewReader(data))
	if err != nil {
		results <- result{err: err}
		return
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	var r map[string]interface{}
	json.Unmarshal(body, &r)
	results <- result{data: r}
}

func main() {
	fmt.Printf("Sending %d concurrent requests (limit is 100)...\n", numRequests)

	client := &http.Client{Timeout: 30 * time.Second}
	results := make(chan result, numRequests)
	var wg sync.WaitGroup

	for i := 1; i <= numRequests; i++ {
		wg.Add(1)
		go sendRequest(i, client, &wg, results)
	}
	wg.Wait()
	close(results)

	successes, concurrencyErrors, otherErrors, exceptions := 0, 0, 0, 0
	for r := range results {
		if r.err != nil {
			exceptions++
		} else if _, ok := r.data["result"]; ok {
			successes++
		} else if e, ok := r.data["error"].(map[string]interface{}); ok {
			if code, _ := e["code"].(float64); int(code) == -32603 {
				concurrencyErrors++
			} else {
				otherErrors++
			}
		}
	}

	fmt.Printf("\nResults:\n")
	fmt.Printf("  Successes:            %d\n", successes)
	fmt.Printf("  Concurrency errors:   %d (code -32603)\n", concurrencyErrors)
	fmt.Printf("  Other errors:         %d\n", otherErrors)
	fmt.Printf("  Exceptions:           %d\n", exceptions)
	fmt.Printf("  Total:                %d\n", successes+concurrencyErrors+otherErrors+exceptions)

	if concurrencyErrors < 1 {
		fmt.Fprintf(os.Stderr, "Expected at least 1 concurrency limit error\n")
		os.Exit(1)
	}
	fmt.Printf("\nConcurrency limit enforced — %d request(s) rejected!\n", concurrencyErrors)
}
