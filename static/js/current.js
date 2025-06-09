async function fetchNowPlaying() {
            const res = await fetch('/api/current_playback');
            const data = await res.json();

            const container = document.getElementById('now-playing');

            container.innerHTML = `
                <h2>Now Playing</h2>
                <img src="${data.image}" alt="Album cover" width="200"><br>
                <strong>${data.track}</strong><br>
                <em>${data.artist}</em><br>
                <small>${data.album}</small><br><br>
                <button onclick="previous()">⏮ Previous</button>
                <button onclick="pause()">⏸ Pause</button>
                <button onclick="play()">▶️ Play</button>
                <button onclick="next()">⏭ Next</button>
            `;
        }

        async function play() {
            await fetch('/playback/play', { method: 'POST' });
            fetchNowPlaying();
        }

        async function pause() {
            await fetch('/playback/pause', { method: 'POST' });
            fetchNowPlaying();
        }

        async function next() {
            await fetch('/playback/next', { method: 'POST' });
            fetchNowPlaying();
        }

        async function previous() {
            await fetch('/playback/previous', { method: 'POST' });
            fetchNowPlaying();
        }

        setInterval(fetchNowPlaying, 500);
        window.onload = fetchNowPlaying;