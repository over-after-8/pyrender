import {createRoot} from "react-dom/client";
import React from "react";
import {useForm} from "react-hook-form"


function AddView({csrf_token}) {

    const {
        register,
        handleSubmit,
        watch,
        formState: {
            errors
        }
    } = useForm({criteriaMode: "all"})

    const watchPassword = watch("password", "")
    const watchConfirmPassword = watch("confirm_password", "")

    const onSubmit = data => {
        document.mainForm.submit()
    }

    return (
        <>
            <div className={"row"}>
                <div className={"col-md-6"}>
                    <form name={"mainForm"} method={"post"} autoComplete={"new-password"}
                          onSubmit={handleSubmit(onSubmit)}>
                        <input type="hidden" className="form-control" name={"csrf_token"} value={csrf_token}></input>
                        <div className="mb-3 form-group">
                            <label>User name</label>
                            <input className="form-control" type="input" placeholder="name@example.com"
                                   name={"user_name"} {...register("user_name", {required: true, maxLength: 63})}/>
                            <div className="invalid-feedback">
                                Please choose a valid username, max length is 63.
                            </div>

                        </div>

                        <div className="mb-3 form-group">
                            <label>Password</label>
                            <input className="form-control" type="password" id={"password"} name={"password"}
                                   {...register("password", {
                                       required: true,
                                       maxLength: 80,
                                       equal: watchConfirmPassword
                                   })}/>
                            <div className="invalid-feedback">
                                Please provide a valid password.
                            </div>

                        </div>

                        <div className="mb-3 form-group">
                            <label>Confirm Password</label>
                            <input className="form-control" type="password" id={"confirm_password"}
                                   name={"confirm_password"}
                                   {...register("confirm_password", {
                                       required: true,
                                       maxLength: 80,
                                       equal: watchPassword
                                   })}
                                   autoComplete={"off"}
                            />
                            <div className="invalid-feedback">
                                Please provide a valid password.
                            </div>
                        </div>

                        <button className={"btn btn-primary me-1"} type={"submit"}><i
                            className="bi bi-save"></i> Save
                        </button>
                        <button className={"btn btn-outline-secondary"} onClick={() => history.back()}><i
                            className="bi bi-x-lg"></i> Cancel
                        </button>
                    </form>
                </div>
            </div>
        </>
    )
}


function App({model, title, csrf_token}) {
    return (
        <>
            <h2>{title}</h2>
            <div className={"mt-4"}>
                <AddView csrf_token={csrf_token}></AddView>
            </div>

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
