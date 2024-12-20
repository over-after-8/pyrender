import {createRoot} from "react-dom/client";
import React, {useState} from "react";
import {CSRFToken} from "./components/utils";
import Datetime from "react-datetime";
import "react-datetime/css/react-datetime.css";


function nowWithoutTime() {
    const date = new Date();
    return date.setHours(0, 0, 0, 0);
}

function AddFormHelper({name, type}) {
    if (type === "Boolean") {
        return (
            <div className="form-check">
                <label>{name}</label>
                <input type="checkbox" className="form-check-input" id="check" name={name}></input>
            </div>
        )
    } else if (type === "TIMESTAMP") {
        const [value, setValue] = useState(nowWithoutTime())
        return (
            <div className={"form-group"}>
                <label>{name}</label>
                <input type={"hidden"} name={name} value={value}/>
                <Datetime dateFormat={"YYYY-MM-DD"} timeFormat={"HH:mm"} onChange={setValue}/>
            </div>
        )
    } else {
        return (
            <div className="form-group">
                <label>{name}</label>
                <input type="text" className="form-control" name={name}></input>
            </div>
        )
    }
}


function AddView({model, csrf_token}) {
    console.log(model)
    return (
        <>
            <div className={"row"}>
                <div className={"col-md-6"}>
                    <form name={"addForm"} className={"smaller-font"} method={"post"}>
                        <CSRFToken csrf_token={csrf_token}></CSRFToken>
                        {
                            model.fields.map((field) => {
                                return (
                                    <div className="mb-3 form-group">
                                        <AddFormHelper name={field.name} type={field.type}/>
                                    </div>
                                )
                            })
                        }

                        <button className={"btn btn-success me-1"} type={"submit"}>
                            <i className="bi bi-plus-lg"></i> Add
                        </button>
                        <button type={"button"} className={"btn btn-outline-danger"} onClick={() => {
                            history.back()
                        }}><i className="bi bi-x-lg"></i> Cancel
                        </button>
                    </form>
                </div>
            </div>
        </>
    )
}


function App({model, title, csrf_token}) {
    const data = JSON.parse(model)
    return (
        <>
            <h2>{title}</h2>
            <AddView model={data} csrf_token={csrf_token}></AddView>
        </>
    )
}


const container = document.getElementById('root_container')
const root = createRoot(container)
const title = document.querySelector('meta[name="title"]').content
const model = document.querySelector('meta[name="model"]').content
const csrf_token = document.querySelector('meta[name="csrf_token"]').content

root.render(
    <App title={title} model={model} csrf_token={csrf_token}/>
)
