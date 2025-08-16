# MarbleElimination
Marble Elimination Simulation

To build web version
- from one directory up, run `uv tool run pygbag --can_close=1 --ume_block=0 --build MarbleElimination`
- output files are in `build/web`

To test locally:
- From root directory, run `python -m http.server`
- In a web browser, open http://127.0.0.1:8000/build/web
- For debugging, open http://127.0.0.1:8000/build/web?-i