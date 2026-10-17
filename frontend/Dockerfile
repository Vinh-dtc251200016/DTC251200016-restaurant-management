# ============================================
# Frontend: Nginx phục vụ static files
# ============================================
FROM nginx:1.25-alpine

# Xóa config mặc định
RUN rm /etc/nginx/conf.d/default.conf

# Copy config Nginx cho frontend
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static files
COPY index.html style.css app.js /usr/share/nginx/html/

# Expose port
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]