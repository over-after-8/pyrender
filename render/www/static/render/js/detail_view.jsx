import {createRoot} from "react-dom/client";
import React from "react";


function ActionBox({actions}) {
    return (
        <>
            <div className="dropdown">
                <button className="btn btn-outline-success dropdown-toggle" type="button" data-bs-toggle="dropdown"
                        aria-expanded="false">
                    Actions
                </button>
                <ul className="dropdown-menu">
                    {
                        Object.keys(actions).map((key, _) => {
                            return <li><a className="dropdown-item" href={actions[key]}>{key}</a></li>
                        })
                    }
                </ul>
            </div>
        </>
    )
}


function ShowViewHelper({value, type}) {

    switch (type) {
        case "Boolean":
            return (
                <div className="form-check">
                    <input className="form-check-input" disabled type="checkbox" checked={value}></input>
                </div>
            )
        case "Relationship":
            if (typeof value === "string") {
                return (
                    <span>{value}</span>
                )
            } else {
                return (
                    <>
                        {
                            value.map((item) => {
                                return <span className="badge text-bg-secondary me-2"
                                             key={`${row_id}_${item}`}>{item}</span>
                            })
                        }
                    </>
                )
            }
        default:
            return (
                <>{value}</>
            )
    }
}

function ShowView({model}) {

    return (
        <>
            {
                Object.keys(model.actions).length !== 0 &&
                <>
                    <ActionBox actions={model.actions}></ActionBox>
                    <br/>
                    <br/>
                </>
            }


            <table className={"table table-striped table-bordered table-hover"}>
                <tbody>
                {model.show_fields.map((field) => {
                    return <tr>
                        <td><strong>{field}</strong></td>
                        <td>
                            <ShowViewHelper value={model.item[field]} type={model.field_types[field]}/>
                        </td>
                    </tr>
                })}
                </tbody>
            </table>
            <button className={"btn btn-outline-secondary"} onClick={() => {
                history.back()
            }}><i className="bi bi-arrow-bar-left"></i> Back
            </button>
        </>
    )
}


function App({model, title}) {
    return (
        <div>
            <h4>{title}</h4>
            <br/>
            <ShowView model={JSON.parse(model)}></ShowView>

        </div>
    )
}


const container = document.getElementById('root_container')
const root = createRoot(container)
const title = document.querySelector('meta[name="title"]').content
const model = document.querySelector('meta[name="model"]').content


root.render(
    <App title={title} model={model}/>
)
