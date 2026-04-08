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

const kubemqURL = "http://localhost:9090"
const basePort = 18080

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

func buildAgents() []map[string]interface{} {
	return []map[string]interface{}{
		{
			"agent_id":    "echo-agent-01",
			"name":        "Echo Agent",
			"description": "Echoes back messages",
			"version":     "1.0.0",
			"url":         fmt.Sprintf("http://localhost:%d/", basePort),
			"skills": []map[string]interface{}{
				{"id": "echo", "name": "Echo", "description": "Echo skill", "tags": []string{"echo", "test"}},
			},
			"defaultInputModes":  []string{"text"},
			"defaultOutputModes": []string{"text"},
			"protocolVersions":   []string{"1.0"},
		},
		{
			"agent_id":    "translate-agent-01",
			"name":        "Translate Agent",
			"description": "Translates text",
			"version":     "1.0.0",
			"url":         fmt.Sprintf("http://localhost:%d/", basePort+1),
			"skills": []map[string]interface{}{
				{"id": "translate", "name": "Translate", "description": "Translation skill", "tags": []string{"translate", "nlp"}},
			},
			"defaultInputModes":  []string{"text"},
			"defaultOutputModes": []string{"text"},
			"protocolVersions":   []string{"1.0"},
		},
		{
			"agent_id":    "summarize-agent-01",
			"name":        "Summarize Agent",
			"description": "Summarizes text",
			"version":     "1.0.0",
			"url":         fmt.Sprintf("http://localhost:%d/", basePort+2),
			"skills": []map[string]interface{}{
				{"id": "summarize", "name": "Summarize", "description": "Summarization skill", "tags": []string{"summarize", "nlp"}},
			},
			"defaultInputModes":  []string{"text"},
			"defaultOutputModes": []string{"text"},
			"protocolVersions":   []string{"1.0"},
		},
	}
}

func main() {
	agents := buildAgents()
	var listeners []net.Listener
	for i, card := range agents {
		port := basePort + i
		mux := http.NewServeMux()
		mux.HandleFunc("/", handler)
		ln, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
		if err != nil {
			fmt.Fprintf(os.Stderr, "Listen failed on port %d: %v\n", port, err)
			os.Exit(1)
		}
		listeners = append(listeners, ln)
		go http.Serve(ln, mux)
		fmt.Printf("Agent '%s' listening on port %d\n", card["agent_id"], port)
	}

	for _, card := range agents {
		data, _ := json.Marshal(card)
		resp, err := http.Post(kubemqURL+"/agents/register", "application/json", bytes.NewReader(data))
		if err != nil {
			fmt.Fprintf(os.Stderr, "Register failed: %v\n", err)
			continue
		}
		resp.Body.Close()
		fmt.Printf("Registered '%s': %d\n", card["agent_id"], resp.StatusCode)
	}

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, os.Interrupt)
	<-sig
	for _, ln := range listeners {
		ln.Close()
	}
	fmt.Println("\nShutting down")
}
