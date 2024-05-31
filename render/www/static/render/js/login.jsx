import {createRoot} from "react-dom/client";
import React from "react";
import {CSRFToken} from "./components/utils";

function App({logo, csrf_token, flashed_messages, url_register}) {

    flashed_messages = flashed_messages.length > 0 && JSON.parse(flashed_messages) || []
    return (
        <>

            <form method="POST" name={"login"}>
                <CSRFToken csrf_token={csrf_token}></CSRFToken>

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

                <div className="form-floating">
                    <input type="email" className="form-control" id="floatingInput" placeholder="name@example.com"
                           name="email"/>
                    <label htmlFor="floatingInput">Email address</label>
                </div>
                <div className="form-floating">
                    <input type="password" className="form-control" id="floatingPassword" placeholder="Password"
                           name="password"/>
                    <label htmlFor="floatingPassword">Password</label>
                </div>

                <div className="form-check text-start my-3">
                    <input className="form-check-input" type="checkbox" value="remember-me" id="flexCheckDefault"
                           name="remember"/>
                    <label className="form-check-label" htmlFor="flexCheckDefault">
                        Remember me
                    </label>
                </div>
                <button className="btn btn-primary w-100 py-2" type="submit">Sign in</button>
                <p className={"mt-2 mb-3"}><a href={url_register}>Don't have an account? Let's create!</a></p>
                <p className="mt-5 mb-3 text-body-secondary">© 2024</p>
            </form>
        </>
    )
}

const container = document.getElementById('root_container')
const root = createRoot(container)
const logo = document.querySelector('meta[name="logo"]').content
const csrf_token = document.querySelector('meta[name="csrf_token"]').content
const flashed_messages = document.querySelector('meta[name="flashed_messages"]').content
const url_register = document.querySelector('meta[name="url_register"]').content

root.render(
    <App logo={logo} csrf_token={csrf_token} flashed_messages={flashed_messages} url_register={url_register}/>
)