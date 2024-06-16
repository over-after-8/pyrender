import {createRoot} from "react-dom/client";
import React, {useState} from "react";
import Select from 'react-select'
import {CSRFToken} from "./components/utils";
import "react-datetime/css/react-datetime.css";
import Datetime from "react-datetime";


function date2timestamp(dateStr) {
    if (dateStr !== null) {
        const split = dateStr.split("-")
        const date = new Date(split[0], split[1] - 1, split[2])
        return date.getTime()
    }
    return ""

}

function EditFormHelper({name, type, initValue, relationships}) {
    switch (type) {
        case "image_upload": {
            return (
                <div>
                    <label htmlFor={`file_${name}`} className="form-label">Default file input example</label>
                    <input className="form-control" type="file" id={`file_${name}`} name={name}/>
                </div>
            )
        }
        case "Date": {
            const [value, setValue] = useState(date2timestamp(initValue))
            return (
                <div>
                    <input type={"hidden"} name={name} value={value}/>
                    <Datetime onChange={setValue} value={value} dateFormat={"YYYY-MM-DD"}
                              timeFormat={false}/>
                </div>
            )
        }

        case "Boolean": {
            const [value, setValue] = useState(Boolean(initValue))
            const onCheckBoxChangeHandler = () => {
                setValue(!value)
            }
            return (
                <input className="form-check-input ms-5" type="checkbox" name={name} checked={value}
                       value={value && 1 || 0}
                       onChange={() => onCheckBoxChangeHandler()}></input>

            )
        }

        case "Relationship": {
            const [value, setValue] = useState(initValue)

            const options = relationships[name].map((item) => {
                return {value: item.id, label: item.name}
            })

            const selectedValue = value.map((item) => {
                return {value: item.id, label: item.name}
            })

            const [selected, setSelected] = React.useState(selectedValue)

            const onSelectChangeHandler = (selected) => {
                setSelected(selected)
                setValue(selected.map((item) => {
                    return {id: item.id, name: item.label}
                }))
            }

            return (
                <>
                    <Select options={options}
                            name={name}
                            closeMenuOnSelect={false}
                            isMulti
                            value={selected} onChange={onSelectChangeHandler}
                    ></Select>
                </>
            )
        }
        default: {
            const [value, setValue] = useState(String(initValue))
            return (
                <input className={"form-control"} name={name} type="input" value={value}
                       onChange={(event) => setValue(event.target.value)}></input>
            )
        }
    }
}

function DisabledEditFormHelper({
                                    type, value
                                }) {
    switch (type) {
        case "Boolean":
            return (
                <input className="form-check-input" type="checkbox" checked={value} value={value && 1 || 0}
                       disabled={true}></input>
            )
        case "Relationship":
            return (
                <>
                    <br/>
                    {
                        value.map((item) => {
                            return <span className="badge text-bg-primary me-1">{item.name}</span>
                        })
                    }
                </>
            )
        default:
            return (
                <input className={"form-control"} type="input" value={value} disabled={true}></input>
            )
    }
}

function EditView({
                      model, csrf_token
                  }) {
    console.log(model)
    return (
        <>
            <div className={"row"}>
                <div className={"col-md-6"}>
                    <form name={"editForm"} className={"smaller-font"} method={"post"} encType={"multipart/form-data"}>
                        <CSRFToken csrf_token={csrf_token}></CSRFToken>
                        {
                            model.disabled_fields.map((field) => {
                                return (
                                    <div className="mb-3 form-group">
                                        <label><strong>{field}</strong></label>
                                        <DisabledEditFormHelper type={model.field_types[field]}
                                                                value={model.item[field][0]}></DisabledEditFormHelper>
                                    </div>
                                )
                            })
                        }
                        {
                            model.edit_fields.map((field) => {
                                return (
                                    <div className="mb-3 form-group">
                                        <label><strong>{field}</strong></label>
                                        <EditFormHelper name={field}
                                                        type={model.field_types[field]}
                                                        initValue={model.item[field][0]}
                                                        relationships={model.relationships}/>
                                    </div>
                                )
                            })
                        }
                        <button className={"btn btn-primary me-2"} type={"submit"}><i
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


function App({
                 model, title, csrf_token
             }) {
    return (
        <>
            <h2>{title}</h2>
            <EditView model={JSON.parse(model)} csrf_token={csrf_token}></EditView>
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
