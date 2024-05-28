import {createRoot} from "react-dom/client";
import React from "react";

const container = document.getElementById('root_container')
const root = createRoot(container)
const logo = document.querySelector('meta[name="logo"]').content
const csrf_token = document.querySelector('meta[name="csrf_token"]').content
const flashed_messages = document.querySelector('meta[name="flashed_messages"]').content

function App({logo, csrf_token, flashed_messages}) {
    flashed_messages = flashed_messages.length > 0 && JSON.parse(flashed_messages) || []

    return (
        <>
            <form method={"POST"} name={"register"}>

                <input type="hidden" name="csrf_token" value={csrf_token}/>

                <img className="mb-4" src={logo} alt=""
                     width="72" height="57"/>
                {
                    flashed_messages.length > 0 &&
                    flashed_messages.map(x => {
                        return <div className="alert alert-danger" role="alert">
                            {x}
                        </div>
                    })
                }
                <h1 className="h3 mb-3 fw-normal">Please sign in</h1>

                <div className="mb-3">
                    <label htmlFor="inputEmail1" className="form-label">Email address</label>
                    <input type="email" className="form-control" id="email" aria-describedby="emailHelp" name={"email"}/>
                    <div id="emailHelp" className="form-text">We'll never share your email with anyone else.</div>
                </div>

                <div className="mb-3">
                    <label htmlFor="inputPassword1" className="form-label">Password</label>
                    <input type="password" className="form-control" id="password" name={"password"}/>
                </div>

                <div className="mb-3">
                    <label htmlFor="inputRepeatPassword1" className="form-label">Repeat Password</label>
                    <input type="password" className="form-control" id="repeatPassword" name={"repeatPassword"}/>
                </div>

                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        </>
    )
}

root.render(
    <App logo={logo} csrf_token={csrf_token} flashed_messages={flashed_messages}/>
)
