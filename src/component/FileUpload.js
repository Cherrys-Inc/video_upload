import React, { useState } from 'react';
import { Upload, Button } from "antd";
import axios from 'axios';
import { useEffect } from 'react';
import "../component/filestyle.css"

export default function FileUpload() {
    

    const [videoSrc , setVideoSrc] = useState("");
    const [urlList,setUrlList] = useState([]);
    const [valid,setValid] = useState(true);
    const [success,setSucess] = useState(false)

    let formData = new FormData();
   
    
    useEffect(() => {
        axios.get('http://localhost:5000/')
        .then(response => {
            setUrlList(response.data)
        })
        .catch(function (error){})
    }, [])
        
        
    const handleChange = ({file}) => {
        
            
        if(file.type === "video/mp4")
        {   
            setValid(true)
            var url = file.originFileObj;
            setVideoSrc(url);
            formData.append("file", videoSrc);
            axios.post('http://localhost:5000',formData,{
            headers: {
                "Content-Type": "multipart/form-data",
            }
            })
            .then(function (response) {
                setSucess(true)
            });
                    
               
        }
        else
        {
            setValid(false)
        }
    };
    
    return (
        
            <div className="action">
                
                <h4>Upload your File</h4>
                <Upload 
                    onChange={handleChange}
                    >
                    <Button>
                       Upload
                    </Button>
                </Upload>
                {!valid? <div className = "alert--text">Please upload a video file</div> : <div></div>}
                {success? <div className = "green--text">File uploaded successfully</div>: <div></div>}
                <div>
                    <h6 className = "head">List of files:</h6>
                    {urlList.map((item,key)=>{
                        return(
                            <ul>
                            <li><a href = {item}>{key}.   {item}</a></li>
                            </ul>
                
                        )
                    })}
                </div>
                

            </div>



    
    )
}
