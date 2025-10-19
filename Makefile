# --- Variables ---

# Local image name (used internally)
IMAGE_NAME := ponti

# Full image name for the Google Artifact Registry (GAR)
# This variable is the target provided in your request.
GAR_REPO := europe-central2-docker.pkg.dev/halogen-rarity-400109/hacktoberfest
GAR_TAG := ponti:latest
FULL_IMAGE_NAME := $(GAR_REPO)/$(GAR_TAG)

# --- Targets ---

.PHONY: build tag push deploy clean all

# Default command: build, tag, and push the image
all: build push

# 1. Build the Docker image locally
build:
	@echo "Building local image: $(IMAGE_NAME)"
	docker build -t $(IMAGE_NAME) .

# 2. Tag the local image with the remote GAR name
tag: build
	@echo "Tagging image for Google Artifact Registry: $(FULL_IMAGE_NAME)"
	docker tag $(IMAGE_NAME) $(FULL_IMAGE_NAME)

# 3. Push the tagged image to the Google Artifact Registry
# Requires you to be authenticated with gcloud/docker.
push: tag
	@echo "Pushing image to Google Artifact Registry..."
	docker push $(FULL_IMAGE_NAME)
	@echo "Deployment complete! Image is available at: $(FULL_IMAGE_NAME)"

# Convenience target to run the local image
run: build
	@echo "Running local image on port 8000..."
	docker run -p 8000:8000 --rm $(IMAGE_NAME)

# Stop and remove the running container
stop:
	@echo "Stopping container..."
	-docker stop $(IMAGE_NAME) || true

# Clean up all generated Docker images
clean: stop
	@echo "Removing local image: $(IMAGE_NAME)"
	-docker rmi $(IMAGE_NAME) || true
	@echo "Removing remote tag image: $(FULL_IMAGE_NAME)"
	-docker rmi $(FULL_IMAGE_NAME) || true