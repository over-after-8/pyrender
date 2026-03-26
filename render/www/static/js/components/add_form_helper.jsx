import React, {useState} from "react";
import {CFormInput, CFormLabel} from "@coreui/react";
import Select from "react-select";

const FormField = ({label, name, children, htmlFor}) => (
    <div className={"mb-3"}>
        <CFormLabel htmlFor={htmlFor}>{label || name}</CFormLabel>
        {children}
    </div>
)


const SelectField = ({name, options, placeholder, isMulti = false}) => {
    const [selected, setSelected] = useState(isMulti ? [] : {value: -1, label: ''})
    const xxx = (e) => {
        console.log(selected)
        setSelected(e)
    }
    return (
        <Select name={name}
                options={options}
                isMulti={isMulti}
                value={selected}
                onChange={xxx}
                placeholder={placeholder || `select ${name}`}
                classNamePrefix={"react-select"}
                closeMenuOnSelect={!isMulti}></Select>
    )
}

const AddFormHelper = ({name, data_type, relationships, select_items}) => {
    const renderInput = () => {
        const relOptions = (relationships?.[name] || []).map((item) => ({
            value: item.id,
            label: item.name,
        }))

        switch (data_type) {
            case "image_upload": {
                return <CFormInput type={"file"} id={`file_${name}`} name={name}></CFormInput>
            }

            case "select": {
                const options = (select_items[name] || []).map((item) => ({
                    value: item,
                    label: item,
                }))
                return <SelectField name={name} options={options}></SelectField>
            }

            case "relationship_one": {
                return <SelectField name={name} options={relOptions}></SelectField>
            }

            case "relationship_many": {
                console.log("relationship_many")
                return <SelectField name={name} options={relOptions} isMulti={true}></SelectField>
            }

            default: {
                return <CFormInput type="text" name={name} placeholder={`type ${name}`}></CFormInput>
            }
        }
    }

    return (
        <FormField label={name} name={name}
                   htmlFor={data_type === `file_upload` ? `file_${name}` : undefined}>
            {renderInput()}
        </FormField>
    )
}

export default AddFormHelper