import { useNavigate } from 'react-router-dom';

const ErrorPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center items-center px-4">
      <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-8 text-center">
        <h1 className="text-4xl font-bold text-black mb-4">404 Not Found</h1>
        <p className="text-xl text-gray-700 mb-6">
          Oops, Something went wrong. The page you're looking for doesn't exist.
        </p>
        <div className="mb-8">
          <svg className="w-24 h-24 mx-auto text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <button
          onClick={() => navigate('/')}
          className=" hover:bg-gray-500 bg-gray-400 text-white font-bold py-2 px-4 rounded transition duration-300 ease-in-out"
        >
          Return to Home
        </button>
      </div>
    </div>
  );
};
export default ErrorPage;