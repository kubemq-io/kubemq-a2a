package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net"
	"net/http"
	"os"
	"os/signal"
)

const (
	kubemqURL = "http://localhost:9090"
	agentID   = "deregister-agent-01"
	agentPort = 18080
)

func handler(w http.ResponseWriter, r *http.Request) {
	var body map[string]interface{}
	json.NewDecoder(r.Body).Decode(&body)
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
		"name":               "Deregister Test Agent",
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
	fmt.Println("Agent registered. Run client.go to test deregistration.")

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, os.Interrupt)
	<-sig
	fmt.Println("\nShutting down")
}
