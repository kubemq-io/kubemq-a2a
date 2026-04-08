package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"os"
	"os/signal"
	"time"
)

const (
	kubemqURL = "http://localhost:9090"
	agentID   = "slow-stream-agent-01"
	agentPort = 18080
)

func handleStream(w http.ResponseWriter, r *http.Request) {
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "streaming not supported", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")

	for i := 1; i <= 10; i++ {
		event, _ := json.Marshal(map[string]interface{}{
			"type": "status_update",
			"payload": map[string]interface{}{
				"status": "working", "progress": i, "total": 10,
			},
		})
		_, err := fmt.Fprintf(w, "event: task.status\ndata: %s\n\n", event)
		if err != nil {
			fmt.Printf("Client disconnected after event %d\n", i-1)
			return
		}
		flusher.Flush()
		fmt.Printf("Sent event %d\n", i)
		time.Sleep(2 * time.Second)
	}

	done, _ := json.Marshal(map[string]interface{}{
		"type":    "done",
		"payload": map[string]interface{}{"final_result": "completed"},
	})
	fmt.Fprintf(w, "event: task.done\ndata: %s\n\n", done)
	flusher.Flush()
}

func handler(w http.ResponseWriter, r *http.Request) {
	var body map[string]interface{}
	json.NewDecoder(r.Body).Decode(&body)

	if method, _ := body["method"].(string); method == "message/stream" {
		handleStream(w, r)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      body["id"],
		"result":  map[string]interface{}{"echo": body},
	})
}

func registerAgent() {
	card := map[string]interface{}{
		"agent_id":           agentID,
		"name":               "Slow Stream Agent",
		"description":        "Emits events slowly for disconnect testing",
		"version":            "1.0.0",
		"url":                fmt.Sprintf("http://localhost:%d/", agentPort),
		"skills":             []interface{}{},
		"defaultInputModes":  []string{"text"},
		"defaultOutputModes": []string{"text"},
		"protocolVersions":   []string{"1.0"},
	}
	data, _ := json.Marshal(card)
	resp, err := http.Post(kubemqURL+"/agents/register", "application/json", bytes.NewReader(data))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Registration failed: %v\n", err)
		return
	}
	resp.Body.Close()
	fmt.Printf("Registered: %d\n", resp.StatusCode)
}

func main() {
	http.HandleFunc("/", handler)

	ln, err := net.Listen("tcp", fmt.Sprintf(":%d", agentPort))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Listen failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Agent listening on port %d\n", agentPort)

	go http.Serve(ln, nil)

	registerAgent()

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, os.Interrupt)
	<-sig
	fmt.Println("\nShutting down")
}
