cleanup() {
    echo ""
    echo "Quit all processes..."
    kill $PID1 $PID2 $PID3 2>/dev/null
    wait $PID1 $PID2 $PID3 2>/dev/null
    echo "Done."
    exit 0
}
trap cleanup SIGINT SIGTERM
ollama serve &
PID1=$!
/usr/bin/python3.11 -m http.server 8080 &
PID2=$!
/usr/bin/python3.11 server.py &
PID3=$!
echo "All processes are running. Ctl+C to quit."
echo "PIDs: ollama=$PID1, http=$PID2, server=$PID3"
wait