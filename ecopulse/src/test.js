import { useState } from 'react';

export default function Example() {
  const [apiKey, setApiKey] = useState('');

  const handleEnter = () => {
    // Here, you can implement the logic to send the `apiKey` to your API
    console.log('Sending API key:', apiKey);
  };

  return (
    <div>
      <label htmlFor="comment" className="block text-sm font-medium leading-6 text-gray-900">
        Enter your API key
      </label>
      <div className="mt-2">
        <textarea
          rows={4}
          name="comment"
          id="comment"
          className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
      </div>
      <button
        className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        onClick={handleEnter}
      >
        Enter
      </button>
    </div>
  );
}
