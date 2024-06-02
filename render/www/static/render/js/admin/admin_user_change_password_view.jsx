import {createRoot} from "react-dom/client";
import React from "react";


function ChangePassword({model, csrf_token}) {
    const [password, setPassword] = React.useState("")
    const [confirmPassword, setConfirmPassword] = React.useState("")
    console.log(model.submit_url)

    const save = () => {
        if (password === confirmPassword) {
            fetch(model.submit_url, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'credentials': 'include',
                    'X-CSRFToken': csrf_token
                },
                body: JSON.stringify({
                    password: password
                })
            }).then(res => {
                console.log(res)
                if (res.status === 200) {
                    alert("Password changed successfully")
                } else {
                    alert("Password changed failed")
                }
            })
        } else {
            alert("Password and confirm password do not match")
        }
    }

    return (
        <>
            <div className={"row"}>
                <div className={"col-md-6"}>
                    <form>
                        <div className="form-group mb-3">
                            <label className={"smaller-font"}>New password</label>
                            <input className={"form-control"} size={"sm"} type="password" onChange={(event) => {
                                setPassword(event.target.value)
                            }}/>
                        </div>
                        <div className="mb-3 form-group">
                            <label className={"smaller-font"}>Confirm password</label>
                            <input className={"form-control"} type="password" onChange={(event) => {
                                setConfirmPassword(event.target.value)
                            }}/>
                        </div>
                        <button className={"btn btn-primary me-2"} onClick={save}><i
                            className="bi bi-save"></i> Save
                        </button>
                        <button type={"button"} className={"btn btn-outline-secondary"} onClick={() => {
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
    const dataModel = JSON.parse(model)
    return (
        <>
            <div className={"d-inline"}>
                <span>{title}:: </span><span>{dataModel.user_name}</span>
            </div>
            <ChangePassword model={dataModel} csrf_token={csrf_token}></ChangePassword>
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
