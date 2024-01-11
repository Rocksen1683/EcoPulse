import React, { useState, useEffect } from 'react';
import leaf from './leaf.png';
function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Example() {
  const [apiKey, setApiKey] = useState('');
  const [csvFile, setCsvFile] = useState(null);
  const [serverFile, setServerFile] = useState(null);
  const [isBaselineLoading, setIsBaselineLoading] = useState(false);
  const [user, setUser] = useState(null);
  const [userSector, setUserSector] = useState(null);

  const handleEnter = async () => {
    const formData = new FormData();
    formData.append('file', csvFile);
    formData.append('fileName', csvFile.name);
    formData.append('apiKey', apiKey);
    setIsBaselineLoading(true);
    const res = await fetch('http://localhost:5000/api/predict', {
      mode: 'cors',
      method: 'POST',
      cache: 'no-cache',
      body: formData,
    }).then((res) => res.json());
    setIsBaselineLoading(false);
    setServerFile(res.filename)
  };
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setCsvFile(file);
  };

  const handleUser = () => {
    fetch('http://localhost:5000/api/user-predict', {
      method: 'POST',
      cache: 'no-cache',
      body: {
        userInfo: user,
        userSector: userSector
      },
    })
  }
  const [apiData, setApiData] = useState(null);

  useEffect(() => {
    // Simulating an API call with setTimeout
    const fetchData = async () => {
      try {
        // Perform your actual API request here
        // Example: const response = await fetch('your-api-endpoint');
        // const data = await response.json();
        // setApiData(data);

        // Simulating API response for demonstration
        setTimeout(() => {
          setApiData({ message: 'API response received!' });
        }, 3000);
      } catch (error) {
        console.error('Error fetching API data:', error);
      }
    };

    fetchData();
  }, []); // The empty dependency array ensures that useEffect runs only once on component mount


  //upon receiving a response from the server, create a new textbox for the user to input their information
    const handleResponse = (response) => {
      const data = response.json();
      console.log(data);
      const input = document.createElement('input');
      input.type = 'text';
      input.placeholder = 'Tell us about yourself, explain what type of investments you are looking for\ne.g. (Im a young investor looking to make big profit, I have a large amount of money to invest and am willing to try anything for a big profit margin and need a return within the next 10 years.)';
      document.body.appendChild(input);
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
        <div>
          <h1 className="text-6xl font-bold tracking-tight text-white sm:text-9xl">
            Eco<br/>Pulse
          </h1>
          <p className="mt-10 text-2xl leading-8 text-dark-green">
            By Cyclic Geese
          </p>
        </div>
        <img className="mx-32" src={leaf} alt="Example" /> 
    </div>

    {/* <img src={leaf} alt="Example" /> */}
  

      {/* inputs */}
   
        </div>
        <div className='px-6'>
          <label className="block text-md mt-20 leading-6 text-dark-green">
            Enter your OpenAI API key
          </label>
          <div className="mt-2">
            <input
              onChange={(e) => setApiKey(e.target.value)}
              className="block w-full rounded-md border-0 px-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            />
          </div>
          <div className="mt-4">
            <label htmlFor="csvFile" className="block text-md mt-20 leading-6 text-dark-green">
              Upload CSV File
            </label>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="block w-full rounded-md border-0 px-3 py-1.5 text-dark-green shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            />
          </div>
          <button
            className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none"
            onClick={handleEnter}
            disabled={isBaselineLoading}
          >
            {isBaselineLoading ? 'Loading...' : 'Enter'}
          </button>

          {isBaselineLoading && (
            <div className="mt-4">
              <p className="text-sm text-gray-500">
                Baseline model loading... please do not refresh the page.
              </p>
            </div>
          )}
          {!isBaselineLoading && serverFile && (
            <div className="mt-4">
              <p className="text-sm text-gray-500">
                Baseline model loaded! Download your file{' '}
                <a
                  href={`http://localhost:5000/api/download/${serverFile}`}
                  className="text-indigo-600 hover:text-indigo-500"
                >
                  here
                </a>
              </p>
            </div>
          )
          }

          {apiData ? (
            <div>
              <label className="block mx-40 text-md mt-20 leading-6 text-dark-green">
                <>
                  <p>Tell us about yourself, explain what type of investments you are looking for<br /></p>
                  <p className='text-grey-400'> (e.g. Im a young investor looking to make big profit, I have a large amount of money to invest and am willing to try anything for a big profit margin and need a return within the next 10 years)</p>
                </>
              </label>
              <div className="mx-40 mt-2">
                <input
                  onChange={(e) => setUser(e.target.value)}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-teal sm:text-sm sm:leading-6"
                />
              </div>
              <label className="block mx-40 text-md mt-20 leading-6 text-dark-green">
              <>
                <p>Tell us more about the type of ideas you want to invest in?<br /></p>
                <p className='text-grey-400'> (e.g. i.e. are you interested in a certain sector (Education), businesss model etc.)</p>
              </>
              </label>
              <div className="mx-40 mt-2">
                <input
                  onChange={(e) => setUserSector(e.target.value)}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-teal sm:text-sm sm:leading-6"
                />
              </div>
              <button
                className="mt-2 mx-40 inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                onClick={handleUser}
              >
                Enter
              </button>
            </div>
            ) : null}
        </div>
      </main>

      {/* Footer */}
      <div className="mx-auto mt-32 max-w-7xl px-6 lg:px-8">
        <footer
          aria-labelledby="footer-heading"
          className="relative border-t border-dark-green py-24 sm:mt-32 sm:py-38"
        >
          <h2 id="footer-heading" className="sr-only">
            Footer
          </h2>
          <h2 className="text-2xl font-bold leading-10 tracking-tight text-gray-900">Thank you to AI EarthHack for inspiring and supporting this project</h2>

        </footer>
      </div>
    </div>
  )
}