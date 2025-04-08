// Custom RAOT admin functionality

// Función para corregir el layout del contenido
function fixContentLayout() {
    // Garantizar que los contenedores de contenido tengan el tamaño correcto
    const contentWrappers = document.querySelectorAll('.content-wrapper');
    contentWrappers.forEach(wrapper => {
        wrapper.style.maxWidth = '100%';
        wrapper.style.overflowX = 'hidden';
        wrapper.style.boxSizing = 'border-box';
        
        // Verificar si hay un contenedor para el contenido
        const contents = wrapper.querySelectorAll('.content');
        contents.forEach(content => {
            let containerExists = content.closest('.content-container');
            
            // Si no hay contenedor, crear uno
            if (!containerExists) {
                const container = document.createElement('div');
                container.className = 'content-container';
                container.style.maxWidth = '1400px';
                container.style.margin = '0 auto';
                container.style.width = '100%';
                container.style.boxSizing = 'border-box';
                
                // Mover el contenido al contenedor
                content.parentNode.insertBefore(container, content);
                container.appendChild(content);
            }
            
            // Asegurar que el contenido tiene las propiedades correctas
            content.style.width = '100%';
            content.style.maxWidth = '100%';
            content.style.boxSizing = 'border-box';
            content.style.margin = '0 auto';
            content.style.padding = '0';
        });
    });
    
    // Corregir filas
    const rows = document.querySelectorAll('.row');
    rows.forEach(row => {
        row.style.width = 'auto';
        row.style.marginLeft = '-15px';
        row.style.marginRight = '-15px';
        row.style.display = 'flex';
        row.style.flexWrap = 'wrap';
        row.style.boxSizing = 'border-box';
        
        // Corregir columnas
        const cols = row.querySelectorAll('[class*="col-"]');
        cols.forEach(col => {
            col.style.padding = '15px';
            col.style.boxSizing = 'border-box';
        });
    });
    
    // Corregir tarjetas
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.width = '100%';
        card.style.boxSizing = 'border-box';
        card.style.marginBottom = '25px';
        
        // Si está dentro de una columna
        const parentCol = card.closest('[class*="col-"]');
        if (parentCol) {
            card.style.height = '100%';
            card.style.marginBottom = '0';
        }
    });
}

// Ejecutar cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', function() {
    fixContentLayout();
    
    // También corregir el layout cuando cambie el tamaño de la ventana
    window.addEventListener('resize', fixContentLayout);
    
    console.log('RAOT Admin JS loaded');
    
    // Add custom welcome message with current date
    const today = new Date();
    const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const dateStr = today.toLocaleDateString('en-US', dateOptions);
    
    const welcomeElement = document.querySelector('.content-header h1');
    if (welcomeElement && welcomeElement.textContent.includes('Dashboard')) {
        welcomeElement.innerHTML = 'RAOT Supplements Dashboard <small class="text-muted d-block mt-2">Welcome to your control panel - ' + dateStr + '</small>';
        
        // Add quick stats cards to dashboard
        const contentInner = document.querySelector('.content');
        if (contentInner) {
            // Get first row of content
            let targetRow = contentInner.querySelector('.row');
            if (!targetRow) {
                targetRow = document.createElement('div');
                targetRow.className = 'row';
                contentInner.prepend(targetRow);
            }
            
            // Add stats cards before the first row
            const statsRow = document.createElement('div');
            statsRow.className = 'row mb-4';
            statsRow.innerHTML = `
                <div class="col-lg-3 col-6">
                    <div class="small-box bg-info">
                        <div class="inner">
                            <h3>Orders</h3>
                            <p>Manage customer orders</p>
                        </div>
                        <div class="icon">
                            <i class="fas fa-shopping-cart"></i>
                        </div>
                        <a href="/admin/checkout/order/" class="small-box-footer">
                            View orders <i class="fas fa-arrow-circle-right"></i>
                        </a>
                    </div>
                </div>
                <div class="col-lg-3 col-6">
                    <div class="small-box bg-success">
                        <div class="inner">
                            <h3>Products</h3>
                            <p>Manage your products</p>
                        </div>
                        <div class="icon">
                            <i class="fas fa-box-open"></i>
                        </div>
                        <a href="/admin/store/product/" class="small-box-footer">
                            View products <i class="fas fa-arrow-circle-right"></i>
                        </a>
                    </div>
                </div>
                <div class="col-lg-3 col-6">
                    <div class="small-box bg-warning">
                        <div class="inner">
                            <h3>Categories</h3>
                            <p>Manage product categories</p>
                        </div>
                        <div class="icon">
                            <i class="fas fa-folder"></i>
                        </div>
                        <a href="/admin/store/category/" class="small-box-footer">
                            View categories <i class="fas fa-arrow-circle-right"></i>
                        </a>
                    </div>
                </div>
                <div class="col-lg-3 col-6">
                    <div class="small-box bg-danger">
                        <div class="inner">
                            <h3>Users</h3>
                            <p>Manage user accounts</p>
                        </div>
                        <div class="icon">
                            <i class="fas fa-users"></i>
                        </div>
                        <a href="/admin/auth/user/" class="small-box-footer">
                            View users <i class="fas fa-arrow-circle-right"></i>
                        </a>
                    </div>
                </div>
            `;
            
            contentInner.prepend(statsRow);
        }
    }
    
    // Enhance product images in admin list view
    if (window.location.href.includes('/admin/store/product/')) {
        const imageCells = document.querySelectorAll('td.field-image');
        imageCells.forEach(cell => {
            const imageUrl = cell.textContent.trim();
            if (imageUrl && !imageUrl.includes('None') && !cell.querySelector('img')) {
                const img = document.createElement('img');
                img.src = imageUrl;
                img.alt = 'Product Image';
                img.classList.add('product-image-preview');
                cell.innerHTML = '';
                cell.appendChild(img);
            }
        });
        
        // Enhance product form
        if (window.location.href.includes('/change/')) {
            // Add preview for image when selected
            const imageField = document.querySelector('input[type="file"][name$="image"]');
            if (imageField) {
                const previewContainer = document.createElement('div');
                previewContainer.className = 'image-preview mt-2';
                previewContainer.style.display = 'none';
                
                const previewImage = document.createElement('img');
                previewImage.style.maxHeight = '200px';
                previewImage.style.maxWidth = '100%';
                previewImage.style.borderRadius = '8px';
                previewImage.style.border = '1px solid #ddd';
                
                previewContainer.appendChild(previewImage);
                imageField.parentNode.appendChild(previewContainer);
                
                imageField.addEventListener('change', function() {
                    const file = this.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            previewImage.src = e.target.result;
                            previewContainer.style.display = 'block';
                        }
                        reader.readAsDataURL(file);
                    } else {
                        previewContainer.style.display = 'none';
                    }
                });
            }
        }
    }
    
    // Add sleek animations to all buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.style.transition = 'all 0.3s ease';
        
        button.addEventListener('mouseover', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
        });
        
        button.addEventListener('mouseout', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // Add branded breadcrumbs
    const breadcrumbs = document.querySelector('.breadcrumb');
    if (breadcrumbs) {
        const firstItem = breadcrumbs.querySelector('li:first-child');
        if (firstItem) {
            const link = firstItem.querySelector('a');
            if (link) {
                link.innerHTML = '<i class="fas fa-home"></i> RAOT Admin';
            }
        }
        
        // Add animation to breadcrumb items
        const breadcrumbItems = breadcrumbs.querySelectorAll('.breadcrumb-item');
        breadcrumbItems.forEach(item => {
            item.style.transition = 'all 0.2s ease';
            
            item.addEventListener('mouseover', function() {
                this.style.transform = 'translateX(3px)';
            });
            
            item.addEventListener('mouseout', function() {
                this.style.transform = 'translateX(0)';
            });
        });
    }
    
    // Add floating labels to form fields for a modern look
    const formControls = document.querySelectorAll('.form-group:not(.multiple-checkbox) label + input.form-control');
    formControls.forEach(input => {
        const label = input.previousElementSibling;
        if (label && label.tagName === 'LABEL') {
            input.placeholder = ' ';
            label.style.position = 'absolute';
            label.style.top = '0';
            label.style.left = '12px';
            label.style.zIndex = '1';
            label.style.padding = '0 5px';
            label.style.backgroundColor = 'white';
            label.style.transform = 'translateY(-50%)';
            label.style.fontSize = '0.85rem';
            label.style.color = '#666';
            
            input.parentElement.style.position = 'relative';
            input.style.paddingTop = '15px';
        }
    });
    
    // Improve form spacing
    const improveFormsSpacing = () => {
        const formGroups = document.querySelectorAll('.form-group');
        formGroups.forEach(group => {
            group.style.marginBottom = '25px';
            
            const label = group.querySelector('label');
            if (label) {
                label.style.marginBottom = '8px';
                label.style.display = 'block';
                label.style.fontWeight = '500';
            }
            
            const input = group.querySelector('input[type="text"], input[type="email"], input[type="number"], textarea');
            if (input) {
                input.style.padding = '10px 15px';
                input.style.lineHeight = '1.5';
            }
        });
        
        const buttons = document.querySelectorAll('.submit-row .button, .submit-row input[type="submit"]');
        buttons.forEach(button => {
            button.style.margin = '0 10px 10px 0';
            button.style.padding = '10px 20px';
        });
    };
    
    // Improve table spacing
    const improveTablesSpacing = () => {
        const tables = document.querySelectorAll('.results, #result_list');
        tables.forEach(table => {
            const headers = table.querySelectorAll('th');
            headers.forEach(header => {
                header.style.padding = '12px 20px';
                header.style.fontWeight = '600';
            });
            
            const cells = table.querySelectorAll('td');
            cells.forEach(cell => {
                cell.style.padding = '15px 20px';
                cell.style.verticalAlign = 'middle';
            });
        });
    };
    
    // Improve filter lists
    const improveFilterLists = () => {
        const filterLists = document.querySelectorAll('#changelist-filter ul');
        filterLists.forEach(list => {
            list.style.margin = '10px 0';
            
            const items = list.querySelectorAll('li');
            items.forEach(item => {
                item.style.padding = '8px 0';
                
                const link = item.querySelector('a');
                if (link) {
                    link.style.display = 'block';
                    link.style.padding = '5px 10px';
                    link.style.borderRadius = '4px';
                }
            });
        });
    };
    
    // Improve dashboard
    const improveDashboard = () => {
        if (window.location.href.includes('/admin/') && !window.location.href.includes('/change')) {
            const modules = document.querySelectorAll('.app-store, .app-auth, .app-checkout, .app-cart, .module');
            modules.forEach(module => {
                module.style.marginBottom = '30px';
                module.style.background = 'white';
                module.style.padding = '20px';
                module.style.borderRadius = '10px';
                module.style.boxShadow = '0 2px 10px rgba(0,0,0,0.05)';
                
                const captions = module.querySelectorAll('caption, h2');
                captions.forEach(caption => {
                    caption.style.padding = '10px 15px';
                    caption.style.fontSize = '16px';
                    caption.style.fontWeight = '600';
                    caption.style.backgroundColor = '#f9f9f9';
                    caption.style.borderRadius = '8px 8px 0 0';
                });
                
                const tableLinks = module.querySelectorAll('table a');
                tableLinks.forEach(link => {
                    link.style.display = 'inline-block';
                    link.style.padding = '3px 0';
                });
            });
        }
    };
    
    // Improve selects
    const improveSelects = () => {
        const selects = document.querySelectorAll('select');
        selects.forEach(select => {
            select.style.minWidth = '200px';
            select.style.height = '42px';
            select.style.padding = '0 10px';
        });
    };
    
    improveFormsSpacing();
    improveTablesSpacing();
    improveFilterLists();
    improveDashboard();
    improveSelects();
    
    // Call the new function
    improveContentSpacing();
    
    // Improve rows and cards
    improveRowsAndCards();
    
    // Reapply in case of dynamic changes
    window.addEventListener('resize', function() {
        improveContentSpacing();
        improveRowsAndCards();
    });
});

// Function to improve main content spacing
const improveContentSpacing = () => {
    // Improve spacing in content areas
    const contentAreas = document.querySelectorAll('.content');
    contentAreas.forEach(content => {
        // Wrap content in a container for centering
        if (!content.parentElement.classList.contains('content-wrapper-inner')) {
            const container = document.createElement('div');
            container.className = 'content-wrapper-inner';
            container.style.maxWidth = '1400px';
            container.style.margin = '0 auto';
            
            // Move content to the new container
            content.parentNode.insertBefore(container, content);
            container.appendChild(content);
        }
        
        // Add more space between main elements
        const mainElements = content.querySelectorAll('.card, .module, fieldset, .inline-group');
        mainElements.forEach(element => {
            element.style.marginBottom = '40px';
        });
    });
    
    // Improve distribution of changelist containers
    const changeListContainers = document.querySelectorAll('#changelist');
    changeListContainers.forEach(container => {
        // Add margins
        container.style.margin = '0 auto';
        
        // Improve sidebar filter
        const filterContainer = container.querySelector('#changelist-filter');
        if (filterContainer) {
            filterContainer.style.padding = '20px';
            filterContainer.style.marginLeft = '25px';
            filterContainer.style.backgroundColor = 'white';
            filterContainer.style.borderRadius = '12px';
            filterContainer.style.boxShadow = '0 3px 15px rgba(0,0,0,0.05)';
            
            // Improve headers
            const headers = filterContainer.querySelectorAll('h2, h3');
            headers.forEach(header => {
                header.style.marginBottom = '20px';
                header.style.padding = '15px';
                header.style.backgroundColor = '#e12e20';
                header.style.color = 'white';
                header.style.borderRadius = '8px';
            });
            
            // Improve lists
            const lists = filterContainer.querySelectorAll('ul');
            lists.forEach(list => {
                list.style.margin = '15px 0';
                
                const items = list.querySelectorAll('li');
                items.forEach(item => {
                    item.style.padding = '10px 0';
                    
                    const link = item.querySelector('a');
                    if (link) {
                        link.style.display = 'block';
                        link.style.padding = '8px 12px';
                        link.style.borderRadius = '6px';
                        link.style.transition = 'all 0.2s ease';
                    }
                });
            });
        }
    });
    
    // Improve forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Identify if it's a main form
        if (form.id === 'changelist-form' || form.classList.contains('change-form')) {
            // Add space around the form
            form.style.margin = '0 auto';
            
            // Improve space between fields
            const formRows = form.querySelectorAll('.form-row');
            formRows.forEach(row => {
                row.style.marginBottom = '25px';
            });
            
            // Improve spacing of submit row
            const submitRow = form.querySelector('.submit-row');
            if (submitRow) {
                submitRow.style.marginTop = '40px';
                submitRow.style.padding = '25px 0';
            }
        }
    });
    
    // Improve result tables
    const resultTables = document.querySelectorAll('.results, #result_list');
    resultTables.forEach(table => {
        // Add rounded borders to the table
        table.style.borderRadius = '10px';
        table.style.overflow = 'hidden';
        
        // Improve headers
        const headers = table.querySelectorAll('th');
        headers.forEach(header => {
            header.style.padding = '16px 24px';
            header.style.backgroundColor = '#f8f8f8';
        });
        
        // Improve cells
        const cells = table.querySelectorAll('td');
        cells.forEach(cell => {
            cell.style.padding = '16px 24px';
            
            // Improve links inside cells
            const links = cell.querySelectorAll('a');
            links.forEach(link => {
                link.style.padding = '3px 6px';
                link.style.borderRadius = '4px';
                link.style.transition = 'all 0.2s ease';
            });
        });
    });
    
    // Improve dashboard modules
    const modules = document.querySelectorAll('.module');
    modules.forEach(module => {
        module.style.marginBottom = '40px';
        module.style.backgroundColor = 'white';
        module.style.borderRadius = '12px';
        module.style.overflow = 'hidden';
        module.style.boxShadow = '0 3px 15px rgba(0,0,0,0.05)';
        
        // Improve tables in modules
        const tables = module.querySelectorAll('table');
        tables.forEach(table => {
            // More spacious cells
            const cells = table.querySelectorAll('td, th');
            cells.forEach(cell => {
                cell.style.padding = '16px 20px';
            });
        });
    });
};

// Function to improve rows and cards
const improveRowsAndCards = () => {
    // Improve rows with cards
    const rows = document.querySelectorAll('.row');
    rows.forEach(row => {
        // Add class for equal height
        row.classList.add('equal-height');
        
        // Find mt-3 cards within the row
        const mtCards = row.querySelectorAll('.card.mt-3');
        if (mtCards.length > 0) {
            // Replace mt-3 with more balanced spacing
            mtCards.forEach(card => {
                card.classList.remove('mt-3');
                card.style.margin = '20px 0';
                
                // Correct padding
                const cardBody = card.querySelector('.card-body');
                if (cardBody) {
                    cardBody.style.padding = '25px';
                }
                
                // Improve internal elements
                const cardTitle = card.querySelector('.card-title');
                if (cardTitle) {
                    cardTitle.style.marginBottom = '20px';
                }
            });
        }
        
        // Correct any column containing cards
        const cardColumns = row.querySelectorAll('[class*="col-"]');
        cardColumns.forEach(column => {
            column.style.padding = '15px';
            
            // Find cards within the column
            const cards = column.querySelectorAll('.card');
            cards.forEach(card => {
                card.style.height = '100%';
                card.style.margin = '0';
                
                // Ensure body occupies full space
                const cardBody = card.querySelector('.card-body');
                if (cardBody) {
                    cardBody.style.height = '100%';
                    cardBody.style.display = 'flex';
                    cardBody.style.flexDirection = 'column';
                }
            });
        });
    });
    
    // Correct especially mt-3 cards outside rows
    const mtCards = document.querySelectorAll('.card.mt-3:not(.row .card)');
    mtCards.forEach(card => {
        card.classList.remove('mt-3');
        card.style.marginTop = '30px';
        card.style.marginBottom = '30px';
    });
    
    // Improve paginator container
    const paginators = document.querySelectorAll('.paginator');
    paginators.forEach(paginator => {
        // Check if it already has a container
        if (!paginator.parentElement.classList.contains('paginator-container')) {
            const container = document.createElement('div');
            container.className = 'paginator-container';
            
            // Wrap paginator in the container
            paginator.parentNode.insertBefore(container, paginator);
            container.appendChild(paginator);
        }
    });
    
    // Redistribute cards that are crowded
    const contentAreas = document.querySelectorAll('.content');
    contentAreas.forEach(content => {
        // Find sequences of cards without proper separation
        const allCards = content.querySelectorAll('.card');
        
        // Check if there are many cards in a row
        const directCardChildren = Array.from(content.children).filter(child => 
            child.classList && child.classList.contains('card')
        );
        
        // If there are more than 2 cards in a row, reorganize them into a grid
        if (directCardChildren.length >= 3) {
            // Create a grid container
            const gridContainer = document.createElement('div');
            gridContainer.className = 'card-grid';
            
            // Move all direct cards to the container
            directCardChildren.forEach(card => {
                content.removeChild(card);
                gridContainer.appendChild(card);
                
                // Reset margins
                card.style.margin = '0';
            });
            
            // Add the grid to the content
            content.appendChild(gridContainer);
        }
    });
};
