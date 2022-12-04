







class ModelFactory:
    def __init__(self,model_config_path:str=None):

        try:
            self.config: dict=ModelFactory.read_params(model_config_path)
            #for calling static function we use classname.function name ex:ModelFactory.read_params
            self.grid_search_cv_module:str=self.config[GRID_SEARCH_KEY][MODULE_KEY]
            self.gird_search_class_name:str=self.config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_search_property_data:dict=dict(self.config[GRID_SEARCH_KEY][PARAM_KEY])

            self.modles_initializaion_config:dict=dict(self.config[MODEL_SELECTION_KEY])

            self.initalized_model_list=None
            self.grid_searched_best_model_list=None 

        except Exception as e:
            raise HousingExcpetion(e,sys) from e

    @staticmethod
    def update_property_of_class(instance_ref:object,property_data:dict):
        try:
            if not isinstance(property_data,dict):
                raise Exception("property parameter required dictionary")
            print(property_data)
            
            for key, value in property_data.items():
                logging.info(f"Executing:$ {str(instance_ref)}.{key}={value}")
                setattr(instance_ref,key,value)
            return instance_ref
        except Exception as e:
            raise HousingExcpetion(e,sys) from e
        
    @staticmethod
    def read_params(config_path:str)->dict:
        try:
            with open(config_path) as yaml_file:
                config:dict=yaml.safe_load(yaml_file) #gives the data in the yaml file as dictionary
            return config
        except Exception as e:
            raise HousingExcpetion(e,sys) from e
    
    @staticmethod
    def class_for_name(module_name:str, class_name:str):
        try:
            #load the module, will raise the Import error if module can not be loaded
            module=importlib.import_module(module_name)
            #get the class, will raise the Attribute Error if class can not be found
            logging.info(f"Executing command : from {module} import {class_name}")
            class_ref=getattr(module,class_name)
            return class_ref
        except Exception as e:
            raise HousingExcpetion(e,sys) from e from e

