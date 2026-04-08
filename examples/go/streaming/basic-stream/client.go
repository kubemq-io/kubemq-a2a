package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
)

const (
	kubemqURL = "http://localhost:9090"
	agentID   = "stream-agent-01"
)

func main() {
	payload := map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      1,
		"method":  "message/stream",
		"params": map[string]interface{}{
			"message": map[string]interface{}{
				"parts": []map[string]interface{}{{"text": "Stream me some updates"}},
			},
		},
	}

	data, err := json.Marshal(payload)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Marshal failed: %v\n", err)
		os.Exit(1)
	}
	req, err := http.NewRequest(http.MethodPost, kubemqURL+"/a2a/"+agentID, bytes.NewReader(data))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request build failed: %v\n", err)
		os.Exit(1)
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "text/event-stream")
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	fmt.Println("Connecting to SSE stream...")
	eventCount := 0
	eventType := ""

	scanner := bufio.NewScanner(resp.Body)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "event: ") {
			eventType = strings.TrimPrefix(line, "event: ")
		} else if strings.HasPrefix(line, "data: ") {
			eventCount++
			dataStr := strings.TrimPrefix(line, "data: ")
			fmt.Printf("[%s] %s\n", eventType, dataStr)
			if eventType == "task.done" || eventType == "task.error" {
				break
			}
		}
	}

	fmt.Printf("\nReceived %d events\n", eventCount)
	fmt.Println("Stream completed!")
}
