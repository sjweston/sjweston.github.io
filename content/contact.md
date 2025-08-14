---
title: 'Data Analysis Consultation'
summary: 'Get in touch for data analysis consultation'
type: page

# Page sections
sections:
  - block: markdown
    content:
      title: Data Analysis Consultation
      text: |
        I'm available to consult on data analysis projects across various domains. 
        Whether you need help with research design, statistical analysis, data visualization, 
        or interpreting results, I'd be happy to discuss your project.
        
        **Areas of expertise include:**
        - Research design and methodology
        - Statistical analysis (descriptive, inferential, predictive)
        - Data visualization and reporting
        - Survey design and analysis
        - Longitudinal data analysis
        - Machine learning applications
        
        Please fill out the form below to get in touch, and I'll respond within 24-48 hours.

  - block: contact
    content:
      title: Consultation Request Form
      subtitle: 'Tell me about your project'
      # Remove personal contact info display
      email: ''
      phone: ''
      address:
        street: ''
        city: ''
        region: ''
        postcode: ''
        country: ''
        country_code: ''
      office_hours: []
      contact_links: []
      # Don't auto-link contact info
      autolink: false
      # Email form provider
      form:
        provider: netlify
        formspree:
          id: ''
        netlify:
          # Enable CAPTCHA challenge to reduce spam?
          captcha: false
        gotenberg:
          # The ID of the form to use
          id: ''
        # Custom form provider
        custom:
          # Custom form action URL
          action: ''
          # Custom form method (POST, GET, etc.)
          method: POST
          # Custom form encoding type
          enctype: application/x-www-form-urlencoded
          # Custom form fields
          fields:
            - name: name
              label: Name
              type: text
              required: true
            - name: email
              label: Email
              type: email
              required: true
            - name: organization
              label: Organization
              type: text
              required: false
            - name: project_type
              label: Project Type
              type: select
              options:
                - Research Design
                - Statistical Analysis
                - Data Visualization
                - Survey Design
                - Machine Learning
                - Other
              required: true
            - name: timeline
              label: Timeline
              type: select
              options:
                - Less than 1 month
                - 1-3 months
                - 3-6 months
                - 6+ months
                - Ongoing
              required: true
            - name: budget
              label: Budget Range
              type: select
              options:
                - Under $1,000
                - $1,000 - $5,000
                - $5,000 - $10,000
                - $10,000+
                - To be discussed
              required: true
            - name: description
              label: Project Description
              type: textarea
              required: true
              placeholder: 'Please describe your project, goals, and any specific questions you have...'
            - name: message
              label: Additional Information
              type: textarea
              required: false
              placeholder: 'Any other details you\'d like to share...'
        # Custom form submit button text
        submit: 'Submit Consultation Request'
        # Custom form success message
        success: 'Thank you for your consultation request! I\'ll review your project details and get back to you within 24-48 hours.'
        # Custom form error message
        error: 'Sorry, there was an error submitting your request. Please try again or email me directly at sara.weston@uoregon.edu'
    design:
      # Single column layout for better form focus
      columns: '1'
---