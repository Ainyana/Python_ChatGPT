import React, { useState, useEffect } from 'react'


function App() {

    const [data, setData] = useState([{}])

    useEffect(() => {
        fetch("/recording").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [])
    return ( < div > {
                (
                    typeof data.recording === 'undefined') ? ( < p > Loading... < /p>) : (
                    data.recording.map((recording, i) => ( < p key = { i } > { recording } < /p>)))
                        } < /div>)
                    }

                    export default App