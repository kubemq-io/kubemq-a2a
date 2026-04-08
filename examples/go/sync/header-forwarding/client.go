package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
)

const (
	kubemqURL = "http://localhost:9090"
	agentID   = "header-agent-01"
)

func main() {
	payload := map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      1,
		"method":  "message/send",
		"params": map[string]interface{}{
			"message": map[string]interface{}{
				"parts": []map[string]interface{}{{"text": "Check my headers"}},
			},
		},
	}

	data, _ := json.Marshal(payload)
	req, _ := http.NewRequest("POST", kubemqURL+"/a2a/"+agentID, bytes.NewReader(data))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Custom-Header", "my-custom-value")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var pretty bytes.Buffer
	json.Indent(&pretty, body, "", "  ")
	fmt.Println(pretty.String())

	var result map[string]interface{}
	json.Unmarshal(body, &result)

	received, _ := result["result"].(map[string]interface{})["received_headers"].(map[string]interface{})
	fmt.Printf("\nForwarded headers: %v\n", received)

	for k := range received {
		if strings.EqualFold(k, "X-Custom-Header") {
			fmt.Println("X-Custom-Header was forwarded successfully!")
		}
		if strings.EqualFold(k, "X-Kubemq-Caller-Id") {
			fmt.Printf("X-KubeMQ-Caller-ID injected: %v\n", received[k])
		}
	}
}
