#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { SpotipyStack } from "../lib/spotipy-stack";

const app = new cdk.App();
new SpotipyStack(app, "SpotipyStack", {});
