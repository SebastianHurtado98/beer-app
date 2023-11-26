import React from 'react';
import { payBills } from '../services/api';

function PayButton({ selectedCustomerId, onPaymentComplete }) {

  const buttonText = selectedCustomerId != null ? 'Pay' : 'Select a customer';
  const handlePayment = () => {
    if (selectedCustomerId) {
      payBills(selectedCustomerId)
        .then((response) => {
          if (response !== null) {
            onPaymentComplete();
          }
        })
        .catch(error => {
          console.error('Error en el pago:', error);
        });
    } else {
      console.log('No hay un cliente seleccionado para realizar el pago');
    }
  };

  return (
    <div>
      <button 
        onClick={handlePayment}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        disabled={!selectedCustomerId}
      >
        {buttonText}
      </button>
    </div>
  );
}

export default PayButton;

