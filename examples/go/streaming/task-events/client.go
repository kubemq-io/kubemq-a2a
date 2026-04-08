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
	agentID   = "task-events-agent-01"
)

func main() {
	payload := map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      1,
		"method":  "message/stream",
		"params": map[string]interface{}{
			"message": map[string]interface{}{
				"parts": []map[string]interface{}{{"text": "Show me all event types"}},
			},
		},
	}

	data, _ := json.Marshal(payload)
	resp, err := http.Post(kubemqURL+"/a2a/"+agentID, "application/json", bytes.NewReader(data))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	fmt.Println("Connecting to SSE stream...")
	eventType := ""
	counts := map[string]int{}

	scanner := bufio.NewScanner(resp.Body)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "event: ") {
			eventType = strings.TrimPrefix(line, "event: ")
		} else if strings.HasPrefix(line, "data: ") {
			counts[eventType]++
			dataStr := strings.TrimPrefix(line, "data: ")

			var d map[string]interface{}
			json.Unmarshal([]byte(dataStr), &d)
			payload, _ := d["payload"].(map[string]interface{})

			switch eventType {
			case "task.status":
				fmt.Printf("  [STATUS]   progress=%.0f/%.0f\n", payload["progress"], payload["total"])
			case "task.artifact":
				fmt.Printf("  [ARTIFACT] name=%v\n", payload["name"])
			case "task.done":
				fmt.Printf("  [DONE]     result=%v\n", payload["final_result"])
			case "task.error":
				fmt.Printf("  [ERROR]    %v\n", payload)
			}

			if eventType == "task.done" || eventType == "task.error" {
				break
			}
		}
	}

	total := 0
	fmt.Println("\n--- Event Summary ---")
	for t, c := range counts {
		fmt.Printf("  %s: %d\n", t, c)
		total += c
	}
	fmt.Printf("  Total: %d\n", total)
}
