/**
 * The ShowcaseProject Model defines the shape of ShowcaseProject data
 * retrieved from the Showcase Service and the API.
 *
 * @author Ajay Gandecha
 * @copyright 2024
 * @license MIT
 */

/** Interface for the Showcase Project */
export interface ShowcaseProject {
  team_name: string;
  type: string;
  members: string[];
  video_url: string;
  deployment_url: string;
}
