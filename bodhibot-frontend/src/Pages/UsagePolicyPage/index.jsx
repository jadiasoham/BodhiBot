import React, { useState, useEffect } from "react";
import axiosService from "../../components/axiosInterceptor";

const baseUrl = process.env.REACT_APP_API_BASE_URL;

const PolicyViewPage = () => {
  const [user, setUser] = useState(null);
  const [policy, setPolicy] = useState(null);
	const [allowed, setAllowed] = useState([]);
	const [blocked, setBlocked] = useState([]);
  const [isEditing, setIsEditing] = useState(false);

  // Fetch user
  const getUser = async () => {
    const response = await axiosService.get(`${baseUrl}auth/me/`);
    if (response?.data) setUser(response.data.data);
  };

  // Fetch policy
  const getPolicy = async () => {
    const response = await axiosService.get(`${baseUrl}chats/usage-policy/`);
    if (response?.data) {
      setPolicy(response.data.policy);
    }
  };

	// Helpers
  const MakeIntoArray = (input) => input?.split(/\r?\n/) || [];
  const ReadFromArray = (arr) => arr.join("\n");

  // Initial load
  useEffect(() => {
    getUser();
    getPolicy();
  }, []);

	// on Policy Change, change the allowed and blocked...
	useEffect(() => {
		let allowedPolicies = policy?.policy?.allowed;
		if (allowedPolicies) setAllowed(allowedPolicies);

		let blockedPolicies = policy?.policy?.blocked;
		if (blockedPolicies) setBlocked(blockedPolicies);
	}, [policy]);

  // Check if user can edit
  const canEdit = user?.is_org_admin || user?.is_superuser;

	if (!user || !policy) return <div>Loading...</div>;

  // Handle save
  const handleSave = async () => {
    try {
      const updatedPolicy = {policy: {allowed: allowed, blocked: blocked}} // parse JSON from textarea
			console.log(updatedPolicy);
      const response = await axiosService.post(
        `${baseUrl}chats/usage-policy/`,
        updatedPolicy
      );
      setPolicy({policy: response.data, updated_on: new Date()}); // update state
      setIsEditing(false);
    } catch (err) {
      console.error("Failed to save policy:", err);
      alert("Failed to save. Make sure the JSON is valid.");
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-md rounded-md">
      <h2 className="text-2xl font-bold mb-2">Usage Policy</h2>
      <p className="text-gray-500 mb-4">
				Last Updated: {policy?.updated_on 
					? new Date(policy.updated_on).toLocaleString("en-IN", {
							day: "2-digit",
							month: "short",
							year: "numeric",
							hour: "2-digit",
							minute: "2-digit",
						})
					: "Unknown"}
			</p>


      {canEdit && !isEditing && (
        <button
          className="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          onClick={() => setIsEditing(true)}
        >
          Edit Policy
        </button>
      )}

      {isEditing ? (
        <div className="space-y-4">
          <div>
            <label className="font-semibold block mb-1">Allowed Actions:</label>
            <textarea
              className="w-full border rounded p-2"
              rows={8}
              value={ReadFromArray(allowed)}
              onChange={(e) => setAllowed(MakeIntoArray(e.target.value))}
            />
          </div>
          <div>
            <label className="font-semibold block mb-1">Blocked Actions:</label>
            <textarea
              className="w-full border rounded p-2"
              rows={8}
              value={ReadFromArray(blocked)}
              onChange={(e) => setBlocked(MakeIntoArray(e.target.value))}
            />
          </div>
          <div className="flex space-x-2">
            <button
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
              onClick={handleSave}
            >
              Save
            </button>
            <button
              className="px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500 transition"
              onClick={() => setIsEditing(false)}
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          <div>
            <h3 className="font-semibold text-lg">You are allowed to:</h3>
            {allowed.length > 0 ? (
              <ul className="list-disc list-inside">
                {allowed.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No allowed actions configured.</p>
            )}
          </div>

          <div>
            <h3 className="font-semibold text-lg">You are <strong>NOT</strong> allowed to:</h3>
            {blocked.length > 0 ? (
              <ul className="list-disc list-inside">
                {blocked.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No blocked actions configured.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default PolicyViewPage;
