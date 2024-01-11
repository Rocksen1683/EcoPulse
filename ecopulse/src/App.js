import React, { useState, useEffect } from 'react';
import WebSocket from 'websocket';
import { Dialog } from '@headlessui/react'
import {
  ArrowPathIcon,
  Bars3Icon,
  CloudArrowUpIcon,
  FingerPrintIcon,
  LockClosedIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline'
import { CheckIcon } from '@heroicons/react/20/solid'


function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Example() {
  const [apiKey, setApiKey] = useState('');
  const [csvFile, setCsvFile] = useState(null);
  const [socket, setSocket] = useState(null);
  const [receivedData, setReceivedData] = useState('');

  const handleEnter = () => {
    const formData = new FormData();
    formData.append('file', csvFile);
    formData.append('fileName', csvFile.name);
    formData.append('apiKey', apiKey);
    fetch('http://localhost:5000/api/predict', {
      method: 'POST',
      cache: 'no-cache',
      body: formData,
    })
  };
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setCsvFile(file);
  };

  useEffect(() => {
    const socket = "localhost:5001/";
    setSocket(socket);

    socket.onopen = () => {
      console.log('WebSocket connection opened');
    };

    socket.onmessage = (event) => {
      setReceivedData(event.data);
      // Here, you can process the received data and update your dashboard
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => {
      // Close the WebSocket connection when the component unmounts
      socket.close();
    };
  }, []);

  return (
    <div className="bg-gradient-to-r from-lime to-teal">

      <main className="isolate">
        {/* Title */}
        <div className="relative pt-14">
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
  
              <div className="mx-auto mx-38 max-w-2xl text-left mt-10">
                <h1 className="text-6xl font-bold tracking-tight text-white sm:text-9xl">
                  Eco<br/>Pulse
                </h1>
                <p className="mt-10 text-2xl leading-8 text-dark-green">
                  By Cyclic Geese
                </p>
              </div>
   
        </div>

      {/* inputs */}
      <div className='mx-40 mt-30'>
      <label className="block text-sm font-medium leading-6 text-gray-900">
        Enter your API key
      </label>
      <div className="mt-2">
        <input
          type="email"
          name="email"
          id="email"
          className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
          placeholder="sk-abc123456789012345678901234567890"
        />
      </div>
      <div className="mt-4">
        <label htmlFor="csvFile" className="block text-sm font-medium leading-6 text-gray-900">
          Upload CSV File
        </label>
        <input
          type="file"
          id="csvFile"
          accept=".csv"
          onChange={handleFileChange}
          className="mt-1 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
        />
      </div>
      <button
        className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        onClick={handleEnter}
      >
        Enter
      </button>
    </div>
    {/* Display received data in a text area */}
    <div className="mt-4">
        <label htmlFor="receivedData" className="block text-sm font-medium leading-6 text-gray-900">
          Received Data
        </label>
        <textarea
          id="receivedData"
          className="mt-1 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
          readOnly
          value={receivedData}
        />
      </div>
      </main>

      {/* Footer */}
      <div className="mx-40 mt-20 max-w-7xl px-6 lg:px-8">
        <footer
          aria-labelledby="footer-heading"
          className="relative border-t border-dark-green py-24 sm:mt-32 sm:py-32"
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

