export default function handler(req, res) {
    if (req.method === 'POST') {
        const callFrom = req.body.From || '';
        const callTo = req.body.To || '';
        const callSid = req.body.CallSid || '';

        // Trả lời JSON để xác nhận đã nhận webhook
        res.status(200).json({
            message: 'Webhook received!',
            callFrom: callFrom,
            callTo: callTo,
            callSid: callSid
        });
    } else {
        // Trả về lỗi nếu không phải là POST request
        res.status(405).json({ message: 'Method not allowed' });
    }
}
