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
	agentID   = "slow-stream-agent-01"
	maxEvents = 2
)

func main() {
	payload := map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      1,
		"method":  "message/stream",
		"params": map[string]interface{}{
			"message": map[string]interface{}{
				"parts": []map[string]interface{}{{"text": "I will disconnect early"}},
			},
		},
	}

	data, _ := json.Marshal(payload)
	resp, err := http.Post(kubemqURL+"/a2a/"+agentID, "application/json", bytes.NewReader(data))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Connecting to stream (will disconnect after %d events)...\n", maxEvents)
	count := 0
	eventType := ""

	scanner := bufio.NewScanner(resp.Body)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "event: ") {
			eventType = strings.TrimPrefix(line, "event: ")
		} else if strings.HasPrefix(line, "data: ") {
			count++
			dataStr := strings.TrimPrefix(line, "data: ")
			var d map[string]interface{}
			json.Unmarshal([]byte(dataStr), &d)
			p, _ := d["payload"].(map[string]interface{})
			fmt.Printf("  Event %d: [%s] progress=%.0f\n", count, eventType, p["progress"])

			if count >= maxEvents {
				fmt.Printf("\nDisconnecting after %d events...\n", maxEvents)
				break
			}
		}
	}
	resp.Body.Close()

	fmt.Println("Client disconnected.")
	fmt.Println("KubeMQ will detect the disconnect and clean up the stream.")
}
