import { Request, Response } from "express";
import axios from "axios";
import * as cheerio from "cheerio";




export class Scrapper {
   async handle(req: Request, res: Response): Promise<Response> {
          try {
            const url = "https://www.itau.com.br/imoveis-itau";
            const response = await axios.get(url);
            const html = response.data;
            const $ = cheerio.load(html);


            const properties: string[] = [];
            $(".property-title-selector").each((_, el) => {
                properties.push($(el).text().trim());
            });
            console.log(properties)

            return res.status(200).json({ properties });
            
        } catch (error) {
            console.log(error);
            return res.status(500).json({ error: "Scraping failed" });
        }
    }
}