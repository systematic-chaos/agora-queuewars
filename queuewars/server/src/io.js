const ioFactory = () => {
    let lastClientId = 0;
    const clients = {};
    return {
        register: (ws) => {
            const clientId = ++lastClientId;
            clients[clientId] = ws;
            return clientId;
        },
        unregister: (clientId) => delete clients[clientId],
        broadcast: (message) => {
            //let encoded_msg = JSON.stringify(message)/*.encode('utf-8')*/;
            /*Object.values(clients).forEach(c => {
                c.send(encoded_msg);
            });*/
            Object.keys(clients).forEach(clientId => {
                clients[clientId].send(JSON.stringify(message));
              });
        }
    };
};

module.exports = { ioFactory };
