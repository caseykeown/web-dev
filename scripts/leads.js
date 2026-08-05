(() => {
  "use strict";

  const WORKER_ENDPOINT = "https://leads-intake.caseykeown.workers.dev/";
  const RECAPTCHA_SITE_KEY = "6LcqDT4tAAAAACr0V9SAU5JCztMLIvz_1bM10jWb";
  const MAX_FILES = 20;
  const MAX_TOTAL_BYTES = 25 * 1024 * 1024;
  const COMPRESS_THRESHOLD = 1.5 * 1024 * 1024;
  const MAX_DIMENSION = 2000;

  const form = document.getElementById("lead-form");
  if (!form) return;

  const steps = [...document.querySelectorAll(".form-step")];
  const stepLabels = [...document.querySelectorAll(".wizard-step-label")];
  const progressFill = document.getElementById("progress-fill");
  const wizardPanel = document.querySelector(".wizard-panel");
  let currentStep = 1;
  let recaptchaWidgetId = null;
  let recaptchaLoadPromise = null;

  const loadRecaptcha = () => {
    if (window.grecaptcha) return Promise.resolve(window.grecaptcha);
    if (recaptchaLoadPromise) return recaptchaLoadPromise;

    recaptchaLoadPromise = new Promise((resolve, reject) => {
      window.onRecaptchaReady = () => resolve(window.grecaptcha);
      const script = document.createElement("script");
      script.src = "https://www.google.com/recaptcha/api.js?onload=onRecaptchaReady&render=explicit";
      script.async = true;
      script.defer = true;
      script.onerror = () => {
        recaptchaLoadPromise = null;
        reject(new Error("reCAPTCHA failed to load"));
      };
      document.head.appendChild(script);
    });

    return recaptchaLoadPromise;
  };

  const renderRecaptcha = async () => {
    if (recaptchaWidgetId !== null) return;
    const container = document.getElementById("recaptcha-container");
    if (!container) return;
    try {
      const grecaptcha = await loadRecaptcha();
      recaptchaWidgetId = grecaptcha.render(container, { sitekey: RECAPTCHA_SITE_KEY });
    } catch (error) {
      console.error(error);
      setStatus("error", "VERIFICATION UNAVAILABLE", "The verification service could not load. Refresh the page and try again.");
    }
  };

  const showStep = (stepNumber, { focus = true } = {}) => {
    currentStep = Math.max(1, Math.min(steps.length, stepNumber));

    steps.forEach((step) => {
      const active = Number(step.dataset.step) === currentStep;
      step.hidden = !active;
      step.classList.toggle("active", active);
    });

    stepLabels.forEach((label) => {
      const active = Number(label.dataset.labelStep) === currentStep;
      label.classList.toggle("active", active);
      if (active) label.setAttribute("aria-current", "step");
      else label.removeAttribute("aria-current");
    });

    progressFill.style.width = `${(currentStep / steps.length) * 100}%`;

    if (currentStep === 3) renderRecaptcha();

    if (focus) {
      const heading = document.querySelector(`.form-step[data-step="${currentStep}"] .step-heading`);
      heading?.setAttribute("tabindex", "-1");
      heading?.focus({ preventScroll: true });
      const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      wizardPanel?.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
    }
  };

  const validateStep = (stepNumber) => {
    const step = document.querySelector(`.form-step[data-step="${stepNumber}"]`);
    const invalid = [...step.querySelectorAll("[required]")].find((field) => !field.checkValidity());
    if (!invalid) return true;
    invalid.reportValidity();
    invalid.focus();
    return false;
  };

  document.querySelectorAll(".next-step").forEach((button) => {
    button.addEventListener("click", () => {
      if (validateStep(currentStep)) showStep(currentStep + 1);
    });
  });

  document.querySelectorAll(".prev-step").forEach((button) => {
    button.addEventListener("click", () => showStep(currentStep - 1));
  });

  let selectedFiles = [];
  let idCounter = 0;

  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const thumbGrid = document.getElementById("thumb-grid");
  const fileCountEl = document.getElementById("file-count");
  const fileSizeTotalEl = document.getElementById("file-size-total");
  const uploadWarning = document.getElementById("upload-warning");

  const showWarning = (message = "") => {
    uploadWarning.textContent = message;
    uploadWarning.hidden = !message;
  };

  const currentTotalBytes = () => selectedFiles.reduce((sum, item) => sum + item.file.size, 0);

  const formatBytes = (bytes) => {
    if (bytes < 1024 * 1024) return `${Math.max(0, bytes / 1024).toFixed(0)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const isImageFile = (file) => file.type.startsWith("image/") || /\.(heic|heif|jpe?g|png|webp|gif)$/i.test(file.name);

  const revokePreview = (item) => {
    if (item.previewUrl) URL.revokeObjectURL(item.previewUrl);
    item.previewUrl = null;
  };

  const checkTotalSize = () => {
    const total = currentTotalBytes();
    if (total > MAX_TOTAL_BYTES) showWarning(`Total photo size (${formatBytes(total)}) exceeds the 25 MB limit. Remove a few photos.`);
  };

  const removeFile = (id) => {
    const item = selectedFiles.find((fileItem) => fileItem.id === id);
    if (item) revokePreview(item);
    selectedFiles = selectedFiles.filter((fileItem) => fileItem.id !== id);
    showWarning();
    renderThumbs();
    checkTotalSize();
  };

  const renderThumbs = () => {
    thumbGrid.replaceChildren();

    selectedFiles.forEach((item) => {
      const wrapper = document.createElement("div");
      wrapper.className = "thumb";

      if (item.compressing) {
        const overlay = document.createElement("div");
        overlay.className = "thumb-compressing";
        overlay.textContent = "Optimizing…";
        wrapper.appendChild(overlay);
      } else {
        revokePreview(item);
        item.previewUrl = URL.createObjectURL(item.file);
        const image = document.createElement("img");
        image.src = item.previewUrl;
        image.alt = "";
        image.loading = "lazy";
        image.addEventListener("error", () => {
          image.replaceWith(Object.assign(document.createElement("div"), {
            className: "thumb-compressing",
            textContent: "Preview unavailable",
          }));
        }, { once: true });
        wrapper.appendChild(image);
      }

      const caption = document.createElement("div");
      caption.className = "thumb-caption";
      caption.textContent = `${item.file.name} · ${formatBytes(item.file.size)}`;
      wrapper.appendChild(caption);

      const removeButton = document.createElement("button");
      removeButton.type = "button";
      removeButton.className = "thumb-remove";
      removeButton.textContent = "×";
      removeButton.setAttribute("aria-label", `Remove ${item.file.name}`);
      removeButton.addEventListener("click", () => removeFile(item.id));
      wrapper.appendChild(removeButton);
      thumbGrid.appendChild(wrapper);
    });

    fileCountEl.textContent = String(selectedFiles.length);
    fileSizeTotalEl.textContent = formatBytes(currentTotalBytes());
  };

  const canvasToBlob = (canvas, type, quality) => new Promise((resolve) => canvas.toBlob(resolve, type, quality));

  const maybeCompressImage = async (file) => {
    const lowerName = file.name.toLowerCase();
    if (file.size <= COMPRESS_THRESHOLD || lowerName.endsWith(".gif")) return file;

    try {
      const bitmap = await createImageBitmap(file);
      let { width, height } = bitmap;
      if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
        const scale = MAX_DIMENSION / Math.max(width, height);
        width = Math.round(width * scale);
        height = Math.round(height * scale);
      }

      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      const context = canvas.getContext("2d", { alpha: true });
      context.drawImage(bitmap, 0, 0, width, height);
      bitmap.close?.();

      const preserveAlpha = /png|webp/i.test(file.type) || /\.(png|webp)$/i.test(lowerName);
      const outputType = preserveAlpha ? "image/webp" : "image/jpeg";
      const blob = await canvasToBlob(canvas, outputType, .82);
      if (!blob || blob.size >= file.size) return file;

      const extension = outputType === "image/webp" ? ".webp" : ".jpg";
      const filename = file.name.replace(/\.[^.]+$/, "") + extension;
      return new File([blob], filename, { type: outputType, lastModified: file.lastModified });
    } catch (error) {
      console.warn("Could not optimize image; using original file:", file.name, error);
      return file;
    }
  };

  const handleIncomingFiles = async (fileList) => {
    const incoming = [...fileList].filter(isImageFile);
    if (!incoming.length) {
      showWarning("Please select image files only.");
      return;
    }

    const remainingSlots = MAX_FILES - selectedFiles.length;
    if (remainingSlots <= 0) {
      showWarning("You have reached the 20-photo limit. Remove a photo to add another.");
      return;
    }

    const toProcess = incoming.slice(0, remainingSlots);
    showWarning(incoming.length > remainingSlots ? `Only ${remainingSlots} additional photo(s) could be added.` : "");

    for (const file of toProcess) {
      const id = `f${idCounter++}`;
      selectedFiles.push({ file, id, compressing: true, previewUrl: null });
      renderThumbs();
      const finalFile = await maybeCompressImage(file);
      const index = selectedFiles.findIndex((item) => item.id === id);
      if (index !== -1) selectedFiles[index] = { file: finalFile, id, compressing: false, previewUrl: null };
      renderThumbs();
    }

    checkTotalSize();
  };

  dropzone.addEventListener("click", () => fileInput.click());
  dropzone.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      fileInput.click();
    }
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropzone.classList.remove("dragover");
    });
  });

  dropzone.addEventListener("drop", (event) => handleIncomingFiles(event.dataTransfer.files));
  fileInput.addEventListener("change", (event) => {
    handleIncomingFiles(event.target.files);
    fileInput.value = "";
  });

  const summaryFields = [
    ["1. Business or organization", "business"],
    ["2. What the business does", "business_description"],
    ["3. Main website purpose", "primary_purpose"],
    ["4. Ideal customer or audience", "target_audience"],
    ["5. Primary visitor action", "primary_action"],
    ["6. Pages needed", "pages_needed"],
    ["7. Priority services or information", "priority_offering"],
    ["8. Special features", "special_features"],
    ["9. Content status", "content_status"],
    ["10. Brand assets", "brand_assets"],
    ["11. Website inspiration", "inspiration_sites"],
    ["12. Existing website/domain/hosting", "existing_web_presence"],
    ["13. Public contact information", "public_contact_info"],
    ["14. Timeline or deadline", "timeline"],
    ["15. Budget and maintenance", "budget"],
  ];

  const buildProjectSummary = () => {
    const ownsDomain = form.querySelector('input[name="owns_domain"]:checked');
    const lines = summaryFields.map(([label, id]) => {
      const field = document.getElementById(id);
      return `${label}:\n${field?.value.trim() || "Not provided"}`;
    });
    lines.splice(12, 0, `Domain/hosting selected answer:\n${ownsDomain?.value || "Not provided"}`);
    return lines.join("\n\n");
  };

  const submitBtn = document.getElementById("submit-btn");
  const statusBanner = document.getElementById("status-banner");
  const statusTitle = document.getElementById("status-title");
  const statusMessage = document.getElementById("status-message");

  function setStatus(type, title, message) {
    statusBanner.hidden = false;
    statusBanner.className = `status-banner ${type}`;
    statusTitle.textContent = title;
    statusMessage.textContent = message;
  }

  function clearStatus() {
    statusBanner.hidden = true;
    statusBanner.className = "status-banner";
    statusTitle.textContent = "";
    statusMessage.textContent = "";
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearStatus();

    if (!form.checkValidity()) {
      const invalid = form.querySelector(":invalid");
      const invalidStep = invalid?.closest(".form-step");
      if (invalidStep) showStep(Number(invalidStep.dataset.step));
      invalid?.reportValidity();
      invalid?.focus();
      return;
    }

    if (currentTotalBytes() > MAX_TOTAL_BYTES) {
      setStatus("error", "UPLOAD TOO LARGE", "The photographs exceed the 25 MB total limit. Remove a few and try again.");
      return;
    }

    if (selectedFiles.some((item) => item.compressing)) {
      setStatus("error", "PLEASE WAIT", "Your photographs are still being optimized.");
      return;
    }

    await renderRecaptcha();
    const recaptchaToken = window.grecaptcha && recaptchaWidgetId !== null ? window.grecaptcha.getResponse(recaptchaWidgetId) : "";
    if (!recaptchaToken) {
      setStatus("error", "VERIFICATION REQUIRED", "Please complete the reCAPTCHA before sending your request.");
      return;
    }

    document.getElementById("project_details").value = buildProjectSummary();
    submitBtn.disabled = true;
    submitBtn.textContent = "Sending…";

    try {
      const formData = new FormData(form);
      selectedFiles.forEach((item) => formData.append("photos", item.file, item.file.name));
      const response = await fetch(WORKER_ENDPOINT, { method: "POST", body: formData });
      const data = await response.json().catch(() => ({ success: false, error: "Unexpected response from the server." }));

      if (!response.ok || !data.success) throw new Error(data.error || "Something went wrong. Please try again.");

      setStatus("success", "REQUEST RECEIVED", "Thank you. Your website request and photographs were received. I will respond within one business day.");
      form.reset();
      selectedFiles.forEach(revokePreview);
      selectedFiles = [];
      renderThumbs();
      showWarning();
      window.grecaptcha?.reset(recaptchaWidgetId);
      statusBanner.focus({ preventScroll: true });
    } catch (error) {
      console.error("Submission failed:", error);
      setStatus("error", "REQUEST NOT SENT", error.message || "The server could not be reached. Check your connection and try again.");
      window.grecaptcha?.reset(recaptchaWidgetId);
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Send Website Request";
    }
  });

  showStep(1, { focus: false });
  renderThumbs();
})();
