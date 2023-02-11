import './App.css';

import { Configuration, OpenAIApi } from "openai";
import { useState } from 'react';

function App() {

  // completion function 
  const completion = async () => {
    fs.createReadStream("src.png")
    // Generate image 
    // const response = await openai.createImageVariation(
    //   fs.createReadStream("src.png"),
    //   3,
    //   "1024x1024"
    // );
    // image_url = response.data.data[0].url;

  }



  return (
    <div className="App mx-auto mt-20 max-w-screen-sm p-7">

      <img className="" src={}></img>
      
    </div>
  );
}

export default App;
