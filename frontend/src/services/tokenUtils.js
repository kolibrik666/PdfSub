// frontend/src/services/tokenUtils.js
import api from './api';

export function decodeTokenUpdateData(token, context) {
    api.decode_token({ token })
        .then(response => {
            const decodedToken = response.data.user;
            context.email = decodedToken.email;
            context.isAdmin = decodedToken.isAdmin;
            context.isParticipant = decodedToken.isParticipant;
            context.isReviewer = decodedToken.isReviewer;
            context.user_id = decodedToken.id;
            console.log(context.isAdmin);
        })
        .catch(error => {
            console.error("Token decoding failed", error.response ? error.response.data : error.message);
            alert("Token decoding failed: " + (error.response ? error.response.data : error.message));
        });
}