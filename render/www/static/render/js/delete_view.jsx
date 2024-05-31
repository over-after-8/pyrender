import {createRoot} from "react-dom/client";
import React from "react";
import {CSRFToken} from "./components/utils";


function DeleteView({csrf_token}) {
    return (
        <>
            <form name={"deleteForm"} method={"post"}>
                <CSRFToken csrf_token={csrf_token}></CSRFToken>
                <div>
                    <label className={"mb-3"}>Are you sure?</label>
                </div>

                <button className={"btn btn-danger me-2"}
                        type={"submit"}><i
                    className="bi bi-trash"></i> Delete
                </button>
                <button className={"btn btn-outline-secondary"} onClick={() => {
                    history.back()
                }}><i className="bi bi-x-lg"></i> Cancel
                </button>
            </form>
        </>
    )
}


function App({title, csrf_token}) {
    return (
        <>
            <h2>{title}</h2>
            <DeleteView csrf_token={csrf_token}></DeleteView>
        </>
    )
}


const container = document.getElementById('root_container')
const root = createRoot(container)
const title = document.querySelector('meta[name="title"]').content
const csrf_token = document.querySelector('meta[name="csrf_token"]').content


root.render(
    <App title={title} model={model} csrf_token={csrf_token}/>
)
