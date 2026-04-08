package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
	"time"
)

const (
	kubemqURL = "http://localhost:9090"
	agentID   = "keepalive-agent-01"
)

func main() {
	payload := map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      1,
		"method":  "message/stream",
		"params": map[string]interface{}{
			"message": map[string]interface{}{
				"parts": []map[string]interface{}{{"text": "Long-running task"}},
			},
		},
	}

	data, _ := json.Marshal(payload)
	client := &http.Client{Timeout: 120 * time.Second}
	resp, err := client.Post(kubemqURL+"/a2a/"+agentID, "application/json", bytes.NewReader(data))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	fmt.Println("Connecting to long-lived SSE stream (expects ~70s with keepalive pauses)...")
	start := time.Now()
	eventType := ""

	scanner := bufio.NewScanner(resp.Body)
	for scanner.Scan() {
		line := scanner.Text()
		elapsed := time.Since(start).Seconds()

		if strings.HasPrefix(line, "event: ") {
			eventType = strings.TrimPrefix(line, "event: ")
		} else if strings.HasPrefix(line, "data: ") {
			dataStr := strings.TrimPrefix(line, "data: ")
			fmt.Printf("  [%6.1fs] [%s] %s\n", elapsed, eventType, dataStr)
			if eventType == "task.done" || eventType == "task.error" {
				break
			}
		} else if strings.HasPrefix(line, ": keepalive") || strings.HasPrefix(line, ":keepalive") {
			fmt.Printf("  [%6.1fs] [keepalive]\n", elapsed)
		}
	}

	total := time.Since(start).Seconds()
	fmt.Printf("\nStream completed in %.1fs\n", total)
	fmt.Println("Keepalive kept the connection alive during long pauses!")
}
