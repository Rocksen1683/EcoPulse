import React, { useState, useEffect } from 'react';
import leaf from './leaf.png';
function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Example() {
  const [apiKey, setApiKey] = useState('');
  const [csvFile, setCsvFile] = useState(null);

  const handleEnter = () => {
    const formData = new FormData();
    formData.append('file', csvFile);
    formData.append('fileName', csvFile.name);
    formData.append('apiKey', apiKey);
    fetch('http://localhost:5000/api/predict', {
      mode: 'cors',
      method: 'POST',
      cache: 'no-cache',
      body: formData,
    })
  };
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setCsvFile(file);
  };

  return (
    <div className="bg-gradient-to-r from-lime to-teal">

      <main className="isolate">
        {/* Title */}
        <div className="mx-40 relative pt-14">
          <div
            className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80"
            aria-hidden="true"
          >
            <div
              className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-green-400 opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
              style={{
                clipPath:
                  'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
              }}
            />
          </div>
          <div className="flex">
    <h1 className="text-6xl font-bold tracking-tight text-white sm:text-9xl">
      Eco<br/>Pulse
    </h1>
    <img className="mx-32" src={leaf} alt="Example" /> 
    </div>
    <p className="mt-10 text-2xl leading-8 text-dark-green">
      By Cyclic Geese
    </p>
    {/* <img src={leaf} alt="Example" /> */}
  

      {/* inputs */}
   
      <label className="block text-md mt-20 leading-6 text-dark-green">
        Enter your API key:
      </label>
      <div className="mt-2">
        <input
          type="email"
          name="email"
          id="email"
          className="block w-full rounded-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-teal sm:text-sm sm:leading-6"
          placeholder=" sk-abc123456789012345678901234567890"
        />
      </div>
      <div className="mt-8">
        <label htmlFor="csvFile" className="block text-md leading-6 text-dark-green">
          Upload CSV File:
        </label>
        <input
          type="file"
          id="csvFile"
          accept=".csv"
          onChange={handleFileChange}
          className="mt-1 block w-full rounded-md border-0 py-1.5 text-dark-green shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
        />
      </div>
      <button
        className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        onClick={handleEnter}
      >
        Enter
      </button>
    </div>
      </main>

      {/* Footer */}
      <div className="mx-40 mt-20 max-w-7xl px-6 lg:px-8">
        <footer
          aria-labelledby="footer-heading"
          className="relative border-t border-dark-green py-24 sm:mt-32 sm:py-38"
        >
          <h2 id="footer-heading" className="sr-only">
            Footer
          </h2>
          <h2 className="text-2xl font-bold leading-10 tracking-tight text-dark-green">Thank you to AI EarthHack for inspiring and supporting this project</h2>

        </footer>
      </div>
    </div>
  )
}