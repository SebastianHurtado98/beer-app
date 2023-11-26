import React from 'react';
import { useState } from 'react';
import { sumUnpaidBillsByCustomer } from '../models/models';

function BillAmount({bills, selectedCustomerId}) {
  const totalAmount = selectedCustomerId != null
  ? sumUnpaidBillsByCustomer(bills, selectedCustomerId)
  : '---';

  return (
    <div>
        <p className="text-9xl my-6">
          {totalAmount}
        </p>
    </div>
  );
}

export default BillAmount;
