package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
)

const (
	kubemqURL   = "http://localhost:9090"
	agentID     = "concurrent-agent-01"
	numRequests = 20
)

type result struct {
	data map[string]interface{}
	err  error
}

func sendRequest(id int, wg *sync.WaitGroup, results chan<- result) {
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
	resp, err := http.Post(kubemqURL+"/a2a/"+agentID, "application/json", bytes.NewReader(data))
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
	fmt.Printf("Sending %d concurrent requests...\n", numRequests)

	results := make(chan result, numRequests)
	var wg sync.WaitGroup

	for i := 1; i <= numRequests; i++ {
		wg.Add(1)
		go sendRequest(i, &wg, results)
	}
	wg.Wait()
	close(results)

	successes, errors, exceptions := 0, 0, 0
	for r := range results {
		if r.err != nil {
			exceptions++
		} else if _, ok := r.data["result"]; ok {
			successes++
		} else if _, ok := r.data["error"]; ok {
			errors++
		}
	}

	fmt.Printf("\nResults:\n")
	fmt.Printf("  Successes:  %d\n", successes)
	fmt.Printf("  Errors:     %d\n", errors)
	fmt.Printf("  Exceptions: %d\n", exceptions)
	fmt.Printf("  Total:      %d\n", successes+errors+exceptions)

	if successes != numRequests {
		fmt.Fprintf(os.Stderr, "Expected %d successes, got %d\n", numRequests, successes)
		os.Exit(1)
	}
	fmt.Printf("\nAll %d concurrent requests completed successfully!\n", numRequests)
}
