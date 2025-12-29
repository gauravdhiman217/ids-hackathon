declare module "critters" {
  export class Critters {
    constructor(options?: Record<string, any>);

    process(html: string): Promise<string>;
  }
}
