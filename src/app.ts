import express from 'express'
import {router} from './routes';
import cors from 'cors'
import {resolve} from 'path'

const app = express()

app.use(cors())
app.use(express.urlencoded({ extended: true}))
app.use(express.json());
app.use(express.static(resolve('uploads')))
app.use(router)

export {app}