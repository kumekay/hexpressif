import React from "react";



class Layout extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            ws: new WebSocket("ws://localhost:8000/ws"),
            hexes: new Map()
        };
        this.black = [0, 0, 0];
    }

    componentDidMount() {
        this.state.ws.addEventListener('open', (event) => {
            this.state.ws.send(JSON.stringify(["sub"]));
            console.log("connected");
        });

        this.state.ws.addEventListener('message', (event) => {
            const json = JSON.parse(event.data);
            console.log(json[0]);
            switch (json[0]) {
                case "layout":
                    this.setLayout(json[1]);
                    break;
                case "board":
                    this.drawBoard(json[1]);
                    break;
                default:
                    console.log(`Unknown WS message: ${json[0]}`)
            }
        });

    }

    componentWillUnmount() {
        if (this.state.ws.readyState === WebSocket.OPEN) {
            // this.state.ws.close();
        }
    }

    setLayout(layout) {
        this.setState({
            "hexes": new Map(layout.map(([q, r]) => [`${q}:${r}`, this.black]))
        });
    }

    drawBoard(board) {
        let hexes = new Map(this.state.hexes);

        board.forEach(([[q, r], v]) => {
            const k = `${q}:${r}`;
            if (hexes.has(k)) {
                hexes.set(k, v);
            }
        })

        this.setState({ hexes })
    }

    render() {
        const coords = (q, r) => {
            const size = 60;
            const sqrt3 = Math.sqrt(3);
            // x, y
            // return [size * (sqrt3 * q + sqrt3 / 2 * r), size * (3. / 2 * r)]
            return [size * (3. / 2 * q), size * (sqrt3 * r + sqrt3 / 2 * q)]
        }

        const hexes = Array.from(this.state.hexes).map(([hex, [r, g, b]]) => {
            const [hq, hr] = hex.split(":");
            const [x, y] = coords(hq, hr);
            return < g transform={`translate(${x},${y})`} >
                <circle cx="0" cy="0" r="48" stroke="#aaa" strokeWidth="2" fill={`rgb(${r},${g},${b})`} />
                <text x="0" y="0" text-anchor="middle" stroke="#aaa" stroke-width="1px" dy=".3em">{hq}, {hr}</text>
            </g >
        }
        );

        return (
            <svg width="100vmin" height="100vmin" viewBox="-500 -500 1000 1000" fill="none" xmlns="http://www.w3.org/2000/svg" >
                {hexes}
            </svg>
        )
    }
}


export default Layout;
