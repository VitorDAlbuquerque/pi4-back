import {app} from './app';

const port = 3333

app.lister(port, () => {
    console.log(`Server started at http://localhost: ${port}`);
})