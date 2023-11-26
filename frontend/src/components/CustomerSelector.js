import React from 'react';

function CustomerSelector({ customers, onCustomerSelect }) {

  const handleSelectChange = (event) => {
    const selectedId = event.target.value;
    if (onCustomerSelect && selectedId) {
      onCustomerSelect(selectedId);
    }
  };

  return (
    <div>
      <select
        className="bg-gray-700 text-white p-2 rounded my-2"
        onChange={handleSelectChange}
        defaultValue=""
      >
        <option value="" disabled>Select a customer</option>
        {customers.map(customer => (
          <option key={customer.id} value={customer.id}>
            {customer.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default CustomerSelector;
