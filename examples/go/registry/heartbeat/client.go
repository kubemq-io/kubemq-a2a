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
	agentID   = "heartbeat-agent-01"
)

func main() {
	for i := 1; i <= 3; i++ {
		body, _ := json.Marshal(map[string]string{"agent_id": agentID})
		resp, err := http.Post(kubemqURL+"/agents/heartbeat", "application/json", bytes.NewReader(body))
		if err != nil {
			fmt.Fprintf(os.Stderr, "Heartbeat failed: %v\n", err)
			os.Exit(1)
		}
		raw, _ := io.ReadAll(resp.Body)
		resp.Body.Close()

		var data map[string]interface{}
		json.Unmarshal(raw, &data)
		fmt.Printf("Heartbeat %d: status=%d last_seen=%v\n", i, resp.StatusCode, data["last_seen"])

		if i < 3 {
			time.Sleep(2 * time.Second)
		}
	}

	fmt.Println("\n=== Final agent state ===")
	resp, _ := http.Get(kubemqURL + "/agents/" + agentID)
	raw, _ := io.ReadAll(resp.Body)
	resp.Body.Close()

	var data map[string]interface{}
	json.Unmarshal(raw, &data)
	fmt.Printf("registered_at: %v\n", data["registered_at"])
	fmt.Printf("last_seen:     %v\n", data["last_seen"])
	fmt.Println("\nHeartbeat cycle completed!")
}
