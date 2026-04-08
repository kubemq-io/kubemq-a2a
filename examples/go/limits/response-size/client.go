package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

const (
	kubemqURL = "http://localhost:9090"
	agentID   = "oversize-agent-01"
)

func main() {
	payload := map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      1,
		"method":  "message/send",
		"params": map[string]interface{}{
			"message": map[string]interface{}{
				"parts": []map[string]interface{}{{"text": "Give me a large response"}},
			},
		},
	}

	data, _ := json.Marshal(payload)
	fmt.Println("Requesting oversized response (>10MB)...")

	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Post(kubemqURL+"/a2a/"+agentID, "application/json", bytes.NewReader(data))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Request failed: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var result map[string]interface{}
	json.Unmarshal(body, &result)

	if errorObj, ok := result["error"].(map[string]interface{}); ok {
		code, _ := errorObj["code"].(float64)
		msg, _ := errorObj["message"].(string)
		fmt.Printf("\nError code:    %.0f\n", code)
		fmt.Printf("Error message: %s\n", msg)
		fmt.Println("\nResponse size limit enforced!")
	} else {
		fmt.Printf("\nStatus: %d\n", resp.StatusCode)
		fmt.Println("Note: Response was accepted (check KubeMQ size limit configuration)")
	}
}
