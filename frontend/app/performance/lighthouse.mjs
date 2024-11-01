/**
 * Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/* eslint-disable @typescript-eslint/explicit-function-return-type */
// @ts-check
import fs from "fs"
import path from "path"

import { LighthouseRunner } from "./LighthouseRunner.mjs"
import { MODES } from "./constants.mjs"

/**
 * The pathname of the current module.
 * @type {string}
 */
const PATHNAME = new URL(".", import.meta.url).pathname

/**
 * The root directory of the Streamlit project.
 * @type {string}
 */
const STREAMLIT_ROOT = path.resolve(PATHNAME, "../../../")

/**
 * The directory containing performance apps.
 * @type {string}
 */
const PERFORMANCE_APPS_DIRECTORY = path.resolve(
  STREAMLIT_ROOT,
  "./e2e_playwright/performance"
)

/**
 * An array of performance app filenames.
 * @type {string[]}
 */
const PERFORMANCE_APPS = fs
  .readdirSync(PERFORMANCE_APPS_DIRECTORY, { withFileTypes: true })
  .filter(entry => {
    return (
      !entry.isDirectory() &&
      entry.name.endsWith(".py") &&
      entry.name !== "__init__.py"
    )
  })
  .map(({ name }) => name)

/**
 * The current timestamp formatted as a string.
 * @type {string}
 */
const NOW = new Date()
  .toISOString()
  .replace(/[-:.TZ]/g, "")
  .slice(0, 15)
  .replace("T", "-")

/**
 * The run ID for the current execution.
 * @type {string}
 */
const RUN_ID = `${NOW.slice(0, 8)}-${NOW.slice(8, 14)}`

const runner = new LighthouseRunner()
await runner.initialize()

process.on("SIGINT", async () => {
  await runner.destroy()
  process.exit(1)
})

try {
  for (const appName of PERFORMANCE_APPS) {
    const appPath = path.join(PERFORMANCE_APPS_DIRECTORY, appName)
    await runner.startStreamlit(appPath, STREAMLIT_ROOT)

    for (const mode of Object.keys(MODES)) {
      await runner.runLighthouse(appName, mode, RUN_ID)
    }

    await runner.stopStreamlit()
  }
} catch (e) {
  console.error(e)
  await runner.destroy()
  process.exit(1)
}

await runner.destroy()
process.exit(0)
