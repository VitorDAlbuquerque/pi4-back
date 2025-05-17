import {Router} from 'express'

const router = Router()

import { Scrapper } from './controllers/Scrapper'

const scrapper = new Scrapper()

router.get("/list", (req, res, next) => {
	scrapper.handle(req, res).catch(next);
})

export {router}