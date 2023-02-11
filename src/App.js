import './App.css';

import { Configuration, OpenAIApi } from "openai";
import { useState } from 'react';

function App() {

  // completion function 
  const completion = async () => {
    
    // Generate image 
    const response = await openai.createImageVariation(
      fs.createReadStream("corgi_and_cat_paw.png"),
      1,
      "1024x1024"
    );
    image_url = response.data.data[0].url;

  }



  return (
    <div className="App mx-auto mt-20 max-w-screen-sm p-7">

      
      
    </div>
  );
}

export default App;
