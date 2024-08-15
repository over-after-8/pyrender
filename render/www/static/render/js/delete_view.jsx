import {createRoot} from "react-dom/client";
import React from "react";
import {CSRFToken} from "./components/utils";


function DeleteView({csrf_token, model}) {
    return (
        <>
            <form name={"deleteForm"} method={"post"}>
                <CSRFToken csrf_token={csrf_token}></CSRFToken>
                <div>
                    <label className={"mb-3"}>Delete {model} item(s)? Are you sure?</label>
                </div>

                <button className={"btn btn-danger me-2"}
                        type={"submit"}><i
                    className="bi bi-trash"></i> Delete
                </button>
                <button type={"button"} className={"btn btn-outline-secondary"} onClick={() => {
                    history.back()
                }}><i className="bi bi-x-lg"></i> Cancel
                </button>
            </form>
        </>
    )
}


function App({title, csrf_token, model}) {
    return (
        <>
            <h2>{title}</h2>
            <DeleteView csrf_token={csrf_token} model={model}></DeleteView>
        </>
    )
}


const container = document.getElementById('root_container')
const root = createRoot(container)
const title = document.querySelector('meta[name="title"]').content
const model = document.querySelector('meta[name="model"]').content
const csrf_token = document.querySelector('meta[name="csrf_token"]').content


root.render(
    <App title={title} csrf_token={csrf_token} model={model}/>
)
